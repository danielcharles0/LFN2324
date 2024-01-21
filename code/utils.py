from IPython.display import Markdown, display

def printCoveredNodes(poi_cat, G, print_=True):
    node_colors = []
    covered_cnt = 0
    poi_cnt = 0
    uncovered_cnt = 0
    nodes = ox.graph_to_gdfs(G, edges=False)
    for index, node in nodes.iterrows():
        if (nodes.at[index, "POI"] == poi_cat):
            node_colors.append("yellow")  
            poi_cnt += 1
        else:
            if nodes.at[index, poi_cat] == True:
                node_colors.append("green")  
                covered_cnt += 1
            else:
                node_colors.append("red")
                uncovered_cnt += 1
    if(print_):
        print("Number of covered nodes (green): ", covered_cnt)
        print("Number of poi nodes (yellow): ", poi_cnt)
        fig, ax = ox.plot_graph(
            G,
            node_color=node_colors,
            node_size=4,
            node_alpha=0.8,
            edge_linewidth=0.2,
            edge_color="#999999",
        )
    return covered_cnt

def printTable(G, subgraph_nodes):
    nodes = ox.graph_to_gdfs(G, edges=False)
    
    s = "<h2>Covered nodes for each category</h2>"
    if(len(constants.CATEGORIES) > 0):
        s +="<table>"
        s +="<tr>"
        s +="<th>Category</th>"
        s +="<th>Num. Covered nodes</th>"
        s +="<th>Percentage of coverage</th>"
        s +="</tr>"
        for c in constants.CATEGORIES:
            s +="<tr>"
            covered = printCoveredNodes(c, G, print_=False)
            percentage = covered * 100 / len(nodes)
            formatted_percentage = round(percentage, 2)
            result_str = str(formatted_percentage)
            s +="<td>"+c+"</td>" 
            s +="<td>"+str(covered)+"</td>" 
            s +="<td>"+result_str+"%</td>" 
            s +="</tr>"
            #print(c, ": " , covered, " covered nodes: %.1f" %(covered*100/len(nodes)), "% of the total"
        s +="</table>"
    s += """
    <h2>Percentage of nodes covered by all categories</h2>
    <p>The following number is a possible representation of how a city is well covered:</p>
    """
    # Save nodes'id that are near all POIs
    near_all_nodes = []
    isolated_nodes = []
    for node, data in G.nodes(data=True):
        near_all = True
        isolated = True
        for category in constants.CATEGORIES:
            covered = data.get(category, False)
            if not covered:
                near_all = False
            else:
                isolated = False
        if near_all:
            near_all_nodes.append(node)
        if isolated:
            isolated_nodes.append(node)
    s +="<table>"
    s +="<tr>"
    s +="<th>Number of covered nodes</th>"
    s +="<th>Total number of nodes</th>"
    s +="<th>Percentage of covered nodes</th>"
    s +="</tr>"
    s +="<tr>"
    percentage = len(near_all_nodes) * 100 / len(nodes)
    formatted_percentage = round(percentage, 2)
    result_str = str(formatted_percentage)
    s +="<td>"+str(len(near_all_nodes))+"</td>" 
    s +="<td>"+str(len(nodes))+"</td>" 
    s +="<td>"+result_str+"%</td>" 
    s +="</tr>"
    s +="</table>"
    s += """
    <h2>Percentage of isolated nodes</h2>
    <p>These are the nodes that are not near any POI:</p>
    """
            
    s +="<table>"
    s +="<tr>"
    s +="<th>Number of isolated nodes</th>"
    s +="<th>Total number of nodes</th>"
    s +="<th>Percentage of isolated nodes</th>"
    s +="</tr>"
    s +="<tr>"
    percentage = len(isolated_nodes) * 100 / len(nodes)
    formatted_percentage = round(percentage, 2)
    result_str = str(formatted_percentage)
    s +="<td>"+str(len(isolated_nodes))+"</td>" 
    s +="<td>"+str(len(nodes))+"</td>" 
    s +="<td>"+result_str+"%</td>"
    s +="</tr>"
    s +="</table>"

    
    display(Markdown(s))
    return near_all_nodes, isolated_nodes