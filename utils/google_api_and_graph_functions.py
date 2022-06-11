from .graphclasses import Node
from .graphclasses import WeightedEdge
from .graphclasses import Digraph
from selenium import webdriver
import requests
from alive_progress import alive_bar
from alive_progress.styles.internal import bar_factory
import time


def get_address_list_from_website(url = 'https://www.google.com/maps/@-23.61706,-46.7304252,12z/data=!4m3!11m2!2s1Rw1gIN0SEkHuw1WBP9X-clVX4p0!3e3'):
    print()
    print('Opening website..............................')
    chromedrive_path = '/Users/bookerschelhaas/Desktop/Code For fun/chromedriver' # use the path to the driver you downloaded from previous steps
    driver = webdriver.Chrome(chromedrive_path)
    #class names are KPxkLd and fKEVAc for names use kiaEld
    driver.get(url)
    time.sleep(.5)
    driver.execute_script("window.scrollTo(0, 1080);")
    time.sleep(3)
    address_list = []
    city_name_raw = driver.find_elements_by_class_name('IFMGgb')[0].text

    print('Scrapping data from website..............................')
    addresses_raw_1 = driver.find_elements_by_class_name('fKEVAc')
    place_names_raw = driver.find_elements_by_class_name('kiaEld')
    city_name_raw = driver.find_elements_by_class_name('IFMGgb')[0].text
    #addresses_raw_2 = driver.find_elements_by_class_name('KPxkLd')
    names = []
    i = 0
    for elem in addresses_raw_1:
        names.append(place_names_raw[i].text)
        #print(place_names_raw[i].text +' ' +elem.text)
        address_list.append(elem.text)
        # if len(elem.text) > 3:
        #     address_list.append(elem.text)
        i += 1
    driver.quit()
    #print(len(names), len(address_list))
    #search for place on google maps and get info
    formatted_addresses = []
    formatted_addresses_dict = {}

    api_file = open('google-api-key')
    api_key = api_file.read()
    api_file.close()

    place_url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?fields=formatted_address%2Cname%2Crating%2Copening_hours%2Cgeometry&'
    
    place_index = 0
    for place in address_list:
        name = names[place_index]
        origin_search = place + ' ' +name + ' ' + city_name_raw 
        #print('search',origin_search )
        r_origin = requests.get(place_url + 'input=' +origin_search + '&inputtype=textquery' +'&key=' + api_key)
        address_formatted = r_origin.json()['candidates'][0]['formatted_address']
        #name = r_origin.json()['candidates'][0]['name']
        formatted_addresses.append(address_formatted)
        formatted_addresses_dict[address_formatted] = name
        #print('place:',name,formatted_addresses[place_index])
        place_index +=1
        
    if len(formatted_addresses) == len(formatted_addresses_dict):
        print('Place information scraped successfully..............................')
    #print(len(formatted_addresses), len(formatted_addresses_dict))
    #print(formatted_addresses_dict, len(formatted_addresses_dict))
    if len(formatted_addresses) == 0:
        print('Scrapping failed. Trying again....')
        formatted_addresses = []
        formatted_addresses_dict = {}
        get_address_list_from_website(url)
    else:
        print()
        return formatted_addresses, formatted_addresses_dict

def get_travel_times(origin,destination,restricted_trans_methods, verbose = False):
    
    ''' This function takes in a origina and destination and uses the google maps API to get 
    travel times for all methods of transportation.

    '''
    api_file = open('google-api-key')
    api_key = api_file.read()
    api_file.close()


    # base dist_url for api
    dist_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&'

    
    # origin_address = origin + ' ' +city
    # dest_address = destination + ' ' + city
    # transportation_modes = ['walking','driving','bicycling','transit']
    # r_origin = requests.get(place_url + 'input=' + origin_address + '&inputtype=textquery' +'&key=' + api_key)
    # origin_address_formatted = r_origin.json()['candidates'][0]['formatted_address']
    # origin_name = r_origin.json()['candidates'][0]['name']
    # r_destination = requests.get(place_url + 'input=' + dest_address  + '&inputtype=textquery' +'&key=' + api_key)
    # dest_address_formatted = r_destination.json()['candidates'][0]['formatted_address']
    # dest_name = r_destination.json()['candidates'][0]['name']
    # get information for place searched
    # r_origin = requests.get(place_url + 'input=' + origin_address + '&inputtype=textquery' +'&key=' + api_key)
    # origin_adress = r_origin.json()['candidates'][0]['formatted_address']
    # if 'rating' in r_origin.json()['candidates'][0]:
    #     origin_rating = r_origin.json()['candidates'][0]['rating']
    # if 'opening_hours' in r_origin.json()['candidates'][0]:
    #     origin_open = r_origin.json()['candidates'][0]['opening_hours']['open_now']

    # r_destination = requests.get(place_url + 'input=' + dest_address  + '&inputtype=textquery' +'&key=' + api_key)
    # destination_adress = r_destination.json()['candidates'][0]['formatted_address']
    # if 'rating' in r_destination.json()['candidates'][0]:
    #     destination_rating = r_destination.json()['candidates'][0]['rating']
    # if 'opening_hours' in r_destination.json()['candidates'][0]:
    #     destination_open = r_destination.json()['candidates'][0]['opening_hours']['open_now']

    # get response for distance
    transportation_modes = ['walking','driving','bicycling','transit']
    travel_times_dict = {}
    for transportation_mode in transportation_modes:
        if transportation_mode in restricted_trans_methods:
            pass
        else:
            r_dist = requests.get(dist_url + "origins=" + origin + '&mode=' + transportation_mode+ '&destinations=' + destination + '&key=' + api_key)

            if r_dist.json()['rows'][0]['elements'][0]['status'] == 'OK':
            #return time as text and as seconds
                time = r_dist.json()['rows'][0]['elements'][0]['duration']['text']
                seconds = r_dist.json()['rows'][0]['elements'][0]['duration']['value']
                travel_times_dict[transportation_mode] = [seconds,time]
                if verbose:
                    print(transportation_mode,time,seconds)
            else:
                print(r_dist.json()['rows'], origin,destination,transportation_mode)
            
    return travel_times_dict



def load_map(address_list,formatted_addresses_dict,restricted_trans_methods = ['transit','bicycling','driving']):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following format, separated by blank spaces:
            From To TotalTime LineColor
        e.g.
            green_st forest_hills 3 orange
        This entry would become an edge from green_st to forest_hills on the orange line. There should also be
        another edge from forest_hills to green_st on the orange line with time travelled = 3

    Returns:
        a directed graph representing the map
    """

    print('Loading map.................')
    T_graph = Digraph() #make a graph instance
    
    i = 0
    custom_bar = bar_factory(tip='⏩', background='🗾🎑🏞️🌅🌄🌠🎇🎆🌇🌁🌉🌌🌃', errors=('😱', '🗡🗡🗡🗡'))
    with alive_bar(len(address_list)*(len(address_list)-1), bar=custom_bar) as bar:
        for add_1 in address_list: 
            new_list_without_add_1 = address_list.copy()
            new_list_without_add_1.remove(add_1)
        
            for add_2 in new_list_without_add_1:
                #print('Progress is ',100*i/(len(address_list)*(len(address_list)-1)),'percent.')
                travel_times_dict = get_travel_times(add_1,add_2,restricted_trans_methods)

                first_node = Node(add_1,formatted_addresses_dict[add_1]) #Node instances
                second_node = Node(add_2,formatted_addresses_dict[add_2])
                if not T_graph.has_node(first_node): # Make sure node is unique in order to add it to set
                    T_graph.add_node(first_node)
                if not T_graph.has_node(second_node):
                    T_graph.add_node(second_node)
                if i == 0:
                    print('Getting travel times........')
                for key in travel_times_dict:
                    time = travel_times_dict[key][0] # change from str to int
                    edge1 = WeightedEdge(first_node,second_node,time,key)
                    edge2 = WeightedEdge(second_node,first_node,time,key)
                    # current_nodes_in_graph = T_graph.get_nodes()
                    # print(current_nodes_in_graph,'lsjflkdsjfa')
                
                
                    current_edges_for_first_node = T_graph.get_edges_for_node(first_node)
                    second_node_edges = T_graph.get_edges_for_node(second_node)
                
                    if edge1 not in current_edges_for_first_node: # add to first node
                        T_graph.add_edge(edge1)
                    if edge2 not in second_node_edges:# add to second node
                        T_graph.add_edge(edge2)
                bar()
                i +=1
    #           print(T_graph.get_edges_for_node(first_node))
    print('--------------Graph complete!------------------')
    return T_graph

def convert_time(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d" % (hour, minutes, seconds)