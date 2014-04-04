import networkx as nx
from collections import Counter
import itertools
import pandas as pd

class MarketBasket:
    
    def __init__(self,data=[],filepath=None,sequential=False):
        """
        Can initialize with properly formatted data
        """
        
        self.data             = data
        self.filepath         = ""
        self.source_headers   = ""
        self.G                = None
        self.transactions     = {}
        self.items            = {}
        self.num_transactions = 0
        self.df               = None
        self.sequential       = sequential
        
        self.item_counts      = {}
        
        if filepath is not None:
            self.load_csv_data(filepath,sequential)
            
    def graph(self):
        """
        Return the NetworkX graph created by the object.
        """
        
        if self.G is None:
            print "No graph has been created."
        else:
            return self.G
    
    def load_data(self,data,sequential=False):
        """
        Data must be in the form
        [[transaction,item,sequence],[transaction,item,sequence]...
        or simply 
        [[transaction,item],[transaction,item]...]
        """
        self.data       = data
        self.sequential = sequential
        
    def load_csv_data(self,filepath,sequential=False,has_headers=True):
        """
        Data should be in the form:
        
        transaction,item,sequence
        transaction,item,sequence
        ...
        """
        
        self.filepath   = filepath
        self.sequential = sequential
        
        f = open(filepath,"r")
        
        if has_headers:
            self.source_headers = f.readline().replace("\n","").strip().split(",")
        
        for line in f:
            line_data = line.replace("\n","").strip().split(",")
            self.data.append(line_data)
        f.close()
        
    def data_head(self,n=5):
        print self.data[:n]
        
    def __establishTransactions(self,maxRuleOrder,includesSequence):
        """
        Internal function to prepare transaction data for 
        other functions. Establishes the self.item_counts dictionary.
        """    
        
        for line in self.data:
            # Keep track of the number of transactions that 
            # each item type appears in. Note that an item 
            # type may appear multiple times in a transaction
            item  = line[1]
            trans = line[0]
            
            if includesSequence:
                seq = line[2]
            
            # Keep a track of how many transactions a particular
            # item appears in. Establish the dictionary for the item
            if not self.item_counts.get(item):
                self.item_counts[item]                 = {}
                self.item_counts[item]['count']        = 0
                self.item_counts[item]['transactions'] = []
            
            # Item has not been included from this transaction yet
            # Use this number for the number of transactions including the item
            if not trans in self.item_counts[item]['transactions']:
                self.item_counts[item]['count'] += 1
                self.item_counts[item]['transactions'].append(trans)
            
            # Keep a count of how many times items appear -- including
            # if they appear multiple times in a single transaction
            if not self.items.get(item):
                self.items[item] = 0
            self.items[item] += 1
            
            # Build a dict of all transactions
            if not self.transactions.get(trans):
                # Initialize the dictionary
                self.transactions[trans]                    = {}
                self.transactions[trans]['sequenced_items'] = []
                self.transactions[trans]['item_count']      = 0
                self.transactions[trans]['single_nodes']    = []
                self.transactions[trans]['multi_nodes']     = []
                self.transactions[trans]['all_nodes']       = []
            
            # Record the item in the dictionary and increment the count
            self.transactions[trans]['single_nodes'].append(item)
            self.transactions[trans]['item_count'] += 1
            
            # In the event that we have the ordering data for a sequence
            # analysis, we want to store the data that indicates the order
            if includesSequence:
                transactions[trans]['sequenced_items'].append((item,seq))
        
        # Keep track of the total number of transactions
        self.num_transactions = len(self.transactions.keys())
        
        
    def build_association_graph(self,maxRuleOrder=2,includesSequence=False):
        """
        This builds a non-sequential association graph. Sequence is not implemented yet.
        """
        
        if self.data == None:
            print "You must load data before building a graph."
            
        self.__establishTransactions(maxRuleOrder,includesSequence)
        
        global_multi_nodes = []
        global_edges       = []
        
        # At this point, the dictionary of transactions is complete
        # and can be iterated to build the combinations of items
        for key in self.transactions.keys():
            # Sort the items
            alpha_singles = sorted(self.transactions[key]['single_nodes'])
            num_items     = self.transactions[key]['item_count']
            
            # Build higher order rule nodes
            if maxRuleOrder > 1:
                for x in range(2,maxRuleOrder + 1):
                    high_order_nodes = [combo for combo in itertools.combinations(alpha_singles,x)]
                    for hon in high_order_nodes:
                        node_name = ""
                        for n in range(x):
                            node_name = node_name + hon[n] + " & "
                        node_name = node_name[:len(node_name) - 3].strip()
                        self.transactions[key]['multi_nodes'].append(node_name)
                        
                        # Count the number of times this combo rule component
                        # appears in the data & track in the same manner as singles
                        if not self.item_counts.get(node_name):
                            self.item_counts[node_name]                 = {}
                            self.item_counts[node_name]['count']        = 0
                            self.item_counts[node_name]['transactions'] = []
                        if not key in self.item_counts[node_name]['transactions']:
                            self.item_counts[node_name]['count'] += 1
                            self.item_counts[node_name]['transactions'].append(key)
            
            # Keep track of higher order nodes in a global list
            global_multi_nodes += self.transactions[key]['multi_nodes']
            self.transactions[key]['all_nodes'] = self.transactions[key]['multi_nodes'] + self.transactions[key]['single_nodes']
            all_sorted = sorted(list(set(self.transactions[key]['all_nodes'])))
            
            # build a list of the edges represented within this transaction - MAYBE SHOULD BE COMBINATIONS
            transaction_edges = [x for x in itertools.permutations(all_sorted,2)]
            global_edges += transaction_edges
            
        # Create the graph object
        self.G = nx.DiGraph(n_transactions = self.num_transactions)
        
        # Build the graph by adding edges
        edge_counter = Counter()
        for e in global_edges:
            edge_counter[e] += 1
        
        # Make sure there is no edge duplication herein
        for e in edge_counter.most_common():
            theedge             = e[0]
            lhs_components_list = theedge[0].replace("&","").split()
            lhs_components      = set(theedge[0].replace("&","").split())
            
            rhs_components_list = theedge[1].replace("&","").split()
            rhs_components      = set(theedge[1].replace("&","").split())
            
            # Exclude rules that have the same thing twice on one side,
            # such as SVG & SVG => CHKING
            if len(lhs_components) < len(lhs_components_list) or len(rhs_components) < len(rhs_components_list):
                continue
            
            # Exclude rules that include shared components on both sides
            if any([i in lhs_components for i in rhs_components]):
                continue
            self.G.add_edge(*theedge,weight=e[1])
            
        # Since I add the nodes by adding the edges, I need to build a 
        # custom dictionary of the node weights, based on nodes preset
        # in the graph after adding edges
        node_weight_dict = {}
        for node in self.G.nodes():
            node_weight_dict[node] = self.item_counts[node]['count']
        
        nx.set_node_attributes(self.G,'weight',node_weight_dict)
    
        return self.G
    
    def associationRules(self,minSupportPercent=5,minConfidencePercent=10):
        """
        Returns a pandas DataFrame with the association rules
        """
        
        theGraph = self.G
        n_trans  = self.num_transactions
        headers  = ["count","rule","LHS","RHS","support(%)","confidence(%)","ex. confidence(%)","lift"]
        rules    = []
        
        for e in theGraph.edges():
            thisRuleRule = e[0] + " => " + e[1]
            thisRuleLHS  = e[0]
            thisRuleRHS  = e[1]
            
            thisEdge = theGraph.edge[thisRuleLHS][thisRuleRHS]
            
            thisLHSWeight  = float(theGraph.node[thisRuleLHS]['weight'])
            thisRHSWeight  = float(theGraph.node[thisRuleRHS]['weight'])
            thisRuleWeight = float(theGraph.edge[thisRuleLHS][thisRuleRHS]['weight'])
            
            thisRuleCount      = thisRuleWeight
            thisRuleSupport    = thisRuleWeight / n_trans
            thisRuleConfidence = thisRuleWeight / thisLHSWeight
            thisRuleExConf     = thisRHSWeight / n_trans
            thisRuleLift       = thisRuleConfidence / (thisRHSWeight/n_trans)
            
            thisRule = [thisRuleCount,thisRuleRule,thisRuleLHS,thisRuleRHS,100*thisRuleSupport,100*thisRuleConfidence,100*thisRuleExConf,thisRuleLift]
            
            # Make sure this is significant enough to keep
            if thisRule[4] >= minSupportPercent and thisRule[5] >= minConfidencePercent:
                rules.append(thisRule)
               
        # Return the data as a Pandas DataFrame
        self.df = pd.DataFrame(rules,columns=headers)
        self.df = self.df.sort(['support(%)'],ascending=[False])
        return self.df

version      = 0.1
release_date = 4/4/2014