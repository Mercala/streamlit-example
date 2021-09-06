#!/usr/bin/env python3.8
# coding: utf-8

pip install fuzzywuzzy

from fuzzywuzzy import fuzz, process, utils
import pandas as pd
import numpy as np
import re
import streamlit as st


def shortest_distance(latlng):
    """Function to find street name based on shortest distance between coordinates"""
    """This function is designed for local street names only!"""
    # Read file with coordinates
    df = pd.read_csv('coordinates.csv')
    df.gac = df.gac.apply(str)
    df_coor = np.array(df[['point_y', 'point_x']].values)

    # Prep coordinates for numpy
    lat, lng = latlng.split(',')
    query = np.array([float(lat.strip()), float(lng.strip())])

    # Compute shortest distant using pitaguras
    shortest_distance = np.sqrt(np.sum((df_coor - query)**2, axis=1))
    index = list(shortest_distance).index(np.min(shortest_distance))

    # Locate street name and number in coordinates file
    return dict(df.iloc[index][:-2])


def sanitize(query):

    dct = {

        # Bad habits
        'nuña'                              : ['nuñe', 'nune'],
        'bucurui'                           : ['boegoeroei', 'boegeroei'],
        'nayostraat'                        : ['yayostraat', 'ayostraat'],
        'blumond'                           : ['bloemond'],
        'koyari'                            : ['korayi'],
        'coribori'                          : ['koeri boeri', 'koeriboeri'],
        'sabania abou'                      : ['sabanilla abao'],
        'jucuri'                            : ['yucuri'],
        'pavilla'                           : ['pavia villas', 'pavia'],
        'kukwisastraat'                     : ['cuquisastraat'],
        'caya mesa bista'                   : ['mesa vista'],
        'paradijswijk'                      : ['paradijsweg'],
        'wayaca'                            : ['wayaka'],
        'barba di yoncumanstraat'           : ['barba di joncuman'],
        'pos chikito'                       : ['pos chquito', 'chiquito'],
        'rooi kochi'                        : ['rooi koochi'],
        'cudawecha'                         : ['kudawecha'],
        'saliña cerca'                      : ['salinja serca', 'salina cerca'],
        'saliña'                            : ['salinja', 'salina'],
        'l.g smith boulevard'               : ['l.g.smith blvd.', 'lg smith blvd', 'lg smith boulevard'],
        'brasil'                            : ['brazil'],
        'diamante'                          : ['gold coast'],
        'sero lopes'                        : ['seroe lopez'],
        'bakval'                            : ['waykiri'],
        'pavilla'                           : ['pavia'],
        'caya soeur rosalie'                : ['seour rosalina'],
        'generaal-majoor de bruynewijk'     : ['g. m. de bruynewijk', 'gm de bruynewijk', 'g m de bruynewijk'],
        'dr. horacio oduber boulevard'      : ['dr. horacio oduber'],
        'caya baranca (tierra del sol)'     : ['caya di baranca', 'caya baranca'],
        'cudi'                              : ['napa valley'],

        # Technical
        '': ['z/n',
        '!',
        '(',
        ')',
        '-',
        'house',
        'new',
        'home',
        'condominiums',
        'condos',
        'condominium',
        'condo',
        ' villa',
        '5 bedroom',
        '4 bedroom',
        '3 bedroom',
        'business opportunity',
        'amazing lot',
        'great opportunity',
        'property land',
        'residence',
        'for sale',
        'luxurious',
        'luxury',
        'family home',
        ' in ',
        'precious estate',
        'beautiful home',
        'charming home',
        'location',
        ' at ',
        'about ',
        'paradise',
        'on the hill',
        'selling',
        'execution value',
        'price',
        'great',
        'investment',
        'reduced',
        'rented',
        'unique',
        'construction',
        'ocean view',
        'penthouse'],
        'ñ': ['ã±'],
        'Ñ': ['Ã±'],

        # Old street names
        #'avenida nelson o. oduber'          : ['sasakiweg'] ,
        'arendstraat'                       : ['caya boes orman'],
        'caya gilberto toppenberg'          : ['marconistraat'],
        'caya ernesto o. petronia'          : ['boerhaavestraat'],
        'caya g.f. betico croes'            : ['nassausstraat'],
        'caya ernesto harms'                : [' lagoenweg'], # Inserted \s not to catch 'Spaanslagoenweg'
        'caya rufo wever'                   : ['willem kloosstraat'],
        'caya ing. roland lacle'            : ['hospitaalstraat'],
        'san barbola complex'               : ['san barbola residence'],
        'avenida milio croes'               : ['fergusonstraat', 'av. milio j. croes'],
        'caya papa juan pablo ii'           : ['rondweg'],
        'caya juancho kock'                 : ['karawarastraat'],
        'caya jose geerman'                 : ['congoweg'],
        'caya lolita e. euson'              : ['tollensstraat'],
        #'sylvia a. goddettstraat'           : ['juliana van stolbergstraat'],
        'nijhoffstraat'                     : ['nijhoff-straat'],
        'caya lolita e. euson'              : ['tollenstraat'],
        #'caya ricardo bernardo statie'      : ['anglostraat'],
    }


    dct_condo = {
        # Condominiums
        'j.e. irausquin boulevard 266'      : ['blue residence', 'blue ', 'blue rentals', 'blue aruba rentals', 'j.e. irausquin boulevard 266', 'je. irausquin boulevard 266', 'je irausquin boulevard 266', 'j e irausquin boulevard 266'],
        'j.e. irausquin boulevard 242'      : ['oasis', 'oasis condominium', 'oasis luxury condominium'],
        'rooi santo 31'                     : ['wariruri', 'wariruri condo', 'wariruri project'],
        'noord 44 Z'                        : ["aruba life condo", "aruba life condominium", "aruba's life condo", "aruba's life condominium", "aruba's life vacation residence", "aruba life residence"],
        'bucurui 43 G'                      : ['isla bunita residence', 'isla bunita condo', 'isla bunita condominium'],
        'diamante'                          : ['costa di solo', 'costa bravo', 'costa bunita', 'djuku', 'caya costa blauw', 'caya santo blanco', 'turtuga', 'gold coast'],
        'weststraat 2'                      : ['harbourhousearuba', 'harbourhouse', 'harbour house', 'harbor house'],
        'j.e. irausquin boulevard 244'      : ['levent', 'le vent', 'levent condominium', 'levent condo', 'le vent condo', 'levent beach resort'],
        'caya dr. j.e.m arends 1'           : ['sunset residence', 'sunset condominium', 'sunset condo'],
        'j.e. irausquin boulevard 252'      : ['atlantic 360', 'atlantic 360 residence', 'atlantic 360 condominium', 'atlantic 360 condo'],
        'j.e. irausquin boulevard 232 B'    : ['the pearl', 'the pearl condominum', 'pearl aruba condo', 'the pearl condo', 'the pearl condo hotel'],
        'j.e. irausquin boulevard 260'      : ['azure', 'azure beach residence', 'azure residence', 'azure luxury condominium', 'azure luxury condo'],
        'j.e. irausquin boulevard 238'      : ['oceania', 'oceania residence', 'oceania aruba rentals', 'oceania deluxe beachfront condominum', 'oceania condominum', 'oceania condo'],
        'dr. horacio oduber boulevard 2'    : ['jardines del mar'],
        'j.e. irausquin boulevard 384 A'    : ['the cove'],
        'palm beach 4'                      : ['palmaruba residence'],
        'j.e. irausquin boulevard 228'      : ['o condominium' , 'o condo'],
        'l.g. smith boulevard 60'           : ['marisol building'],
        'caya baranca 20 D'                 : ['las rocas', 'las rocas condominum', 'las rocas condo'],
        'rooi santo'                        : ['aracari residence'],
        'j.e. irausquin boulevard 232'      : ['aruba breeze condominium', 'aruba breeze condo', 'aruba breeze']
    }

    for k, v in dct_condo.items():
        for i in v:
            if i in query:
                query = k

    for k, v in dct.items():
        for i in v:
            if i in query:
                query = query.replace(i, k)

    return query



def street_name(query, tolerance=100):

    df = pd.read_csv('coordinates.csv')
    df.gac = df.gac.apply(str)
    df.sort_values('street_name', inplace=True)
    df.drop_duplicates(subset='street_name', keep='first', inplace=True)

    # Replace erroneous streetnames
    query = sanitize(query)

    # Extract house number and suffix
    original = re.findall(r'\b\d+\W*\w?\b', query)
    num_and_suff = re.findall(r'\b(\d+)\W*(\w?)\b', query)
    num_and_suff = [' '.join(i).upper() for i in num_and_suff]

    if num_and_suff:
        num_and_suff = num_and_suff[0].strip()
    else:
        num_and_suff = ''

    # Remove AddNum & AddNumSuffix from street name
    for i in original:
        query = query.replace(i, '').strip()

    if utils.full_process(query):
        # Compare query to address list and get closest match
        top_choice = process.extractOne(query, df['street_name'].values, score_cutoff=tolerance)

        if top_choice:
            # Get the index of the closest match
            index = list(df['street_name'].values).index(top_choice[0])
            # Extract street_name, neighborhood, district and gac code
            lst_address = list(df.iloc[index, [0, 2, 3, 4]].values)
            # Add house number and suffix back to the address
            lst_address.insert(1, num_and_suff)

            dct = dict(zip(['street_name', 'house_number', 'neighborhood', 'district', 'gac'], lst_address))

            return dct
            # These were all set to ''
        return {'street_name': '', 'house_number': '', 'neighborhood': '', 'district': '', 'gac': ''}

    return {'street_name': '', 'house_number': '', 'neighborhood': '', 'district': '', 'gac': ''}



# Streamlit
st.title('Aruba Complete Adresses')
user_input = st.text_input('Enter street name and house number', 'Magdalenastraat 3')

result = street_name(user_input, 80)
st.write('\n')
st.write('Copy/Paste the full address below:')
st.text(f"{result['street_name']} {result['house_number']}\n{result['neighborhood']}\n{result['district']}\n{result['gac']} Aruba")
