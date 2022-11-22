#!/usr/bin/env python3
import os
import sys
import logging
import joblib
import numpy as np
import pandas as pd
logging.disable(logging.WARNING)
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from keras.models import load_model


from scapy.all import (
    TCP,
    FieldLenField,
    FieldListField,
    IntField,
    IPOption,
    ShortField,
    get_if_list,
    sniff
)
from scapy.layers.inet import _IPOption_HDR


global list_packet , old_dataframe



def get_if():
    ifs=get_if_list()
    iface=None
    for i in get_if_list():
        if "eth0" in i:
            iface=i
            break;
    if not iface:
        print("Cannot find eth0 interface")
        exit(1)
    return iface

class IPOption_MRI(IPOption):
    name = "MRI"
    option = 31
    fields_desc = [ _IPOption_HDR,
                    FieldLenField("length", None, fmt="B",
                                  length_of="swids",
                                  adjust=lambda pkt,l:l+4),
                    ShortField("count", 0),
                    FieldListField("swids",
                                   [],
                                   IntField("", 0),
                                   length_from=lambda pkt:pkt.count*4) ]

def naive_bayes_module(data , nb_module):
    x_classification = data[['proto', 'lstm_result_1','lstm_result_2']]
    prediction = nb_module.predict(x_classification)
    x_classification = pd.DataFrame(x_classification)
    x_classification['label'] = pd.DataFrame(prediction)
    return x_classification

def preprocessing_module(data,le, norm):
    data_check = pd.DataFrame()
    le.fit(data.src)
    data_check['src'] = le.transform(data['src'])
    le.fit(data.dst)
    data_check['dst'] = le.transform(data['dst'])
    le.fit(data.proto)
    data_check['proto'] = le.transform(data['proto'])
    data_check['len'] = data['len']
    data_check['count_packet'] = data['count_packet']
    #data_check = np.reshape(data_check, (1,-1))
    #data_check = norm.fit_transform(data_check)
    return data_check


def lstm_module(lstm_model, data):
    x_train = data
    x_train_awal = x_train
    x_train = x_train.to_numpy()
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    y_pred_train = lstm_model.predict(x_train)
    y_pred_train_1 = [x[0] for x in y_pred_train]
    y_pred_train_2 = [x[1] for x in y_pred_train]

    df_x_train = x_train_awal
    df_x_train['lstm_result_1'] = y_pred_train_1
    df_x_train['lstm_result_2'] = y_pred_train_2
    return df_x_train

    # data = np.array([[pkt.src,pkt.dst,pkt.len, pkt.proto]])
    # data = pd.DataFrame(data, columns=['src','dst','len','proto'])
    # #label encoding module library
    # le = LabelEncoder()
    # #normalizaiton module library
    # norm = MinMaxScaler()
    # data_check = preprocessing_module(data, le, norm)
    # #data_check = np.reshape(data_check, (-1, 4))
    # klasifikasi = lstm_model(lstm_model, data_check)
    # #klasifikasi = naive_bayes_module(data_check, model_predict)
    # print(klasifikasi)

def making_statistics(data, old_dataframe):
    data_akhir = pd.DataFrame()
    # Get Distinct SRC dan DST
    data_stat = data.groupby(['src','dst', 'proto'], as_index=False).size()
    data_sum = data.groupby(['src','dst', 'proto'], as_index=False).sum('len')

    
    data_akhir['src'] = data_stat['src']
    data_akhir['dst'] = data_stat['dst']
    data_akhir['proto'] = data_stat['proto']
    data_akhir['count_packet'] =  data_stat['size'] + old_dataframe['count_packet']
    data_akhir['len'] = data_sum['len'] + old_dataframe['len']
    return data_akhir


def handle_pkt(pkt, list_packet, lstm_model, nb_model, le, norm, old_dataframe):
    try:
        if len(list_packet) == 20:
            data = pd.DataFrame(list_packet, columns=['src','dst','len','proto'])
            # Making Data Statistics
            data = making_statistics(data, old_dataframe)
            #old Value
            old_dataframe['count_packet'] += data['count_packet']
            old_dataframe['len'] += data['len']
            # Prediction
            data_check = preprocessing_module(data, le, norm)
            lstm_klasifikasi = lstm_module(lstm_model, data_check)
            prediction = naive_bayes_module(lstm_klasifikasi, nb_model)
            prediction['src'] = data['src']
            prediction['dst'] = data['dst']
            
            #Printing Result
            #print(prediction)
            for index, row in prediction.iterrows():
                if row['label'] == 1:
                    print(f"Network SRC = {row['src']} dengan DST = {row['dst']} Terklasifikasi Intrusi")
                else :
                   print(f"Network SRC = {row['src']} dengan DST = {row['dst']} Terklasifikasi Normal")

            # Reset
            list_packet = list()
            list_packet.append([pkt.src,pkt.dst,pkt.len, pkt.proto])
        else: 
            list_packet.append([pkt.src,pkt.dst,pkt.len, pkt.proto])

    except:
        list_packet.append([0,0,0,0])


    # if TCP in pkt and pkt[TCP].dport == 1234:
    # print(pkt.src)
    # print(pkt.dst)
    # print(pkt.len)
    # print(pkt.proto)
    #pkt.show2()
    #lambda x: 

def sniffing_data(iface):
    counter = 0
    list_packet = list()
    lstm_model = load_model('lstm_slice.h5')
    nb_model = joblib.load('naive_bayes_final.pkl')
    le = LabelEncoder()
    norm = MinMaxScaler()
    #making dataframe with 20 data
    old_dataframe = pd.DataFrame([[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]], columns=['src','dst','proto', 'count_packet', 'len'])
    sniff(iface = iface, prn = lambda x:handle_pkt(x, list_packet, lstm_model, nb_model, le, norm, old_dataframe))
       



def main():
    print('Welcome to LSTM-NB DoS Detection System')
    print('Silahkan Pilih Network Interface')
    ifaces = [i for i in os.listdir('/sys/class/net/') if 'eth' in i]
    index = 1
    for x in ifaces:
        print("[%s].  %s" %(index, x))
        index+=1
    var_input = int(input('Masukkan Pilihan Anda : '))
    iface = ifaces[var_input-1]
    print("sniffing on %s" % iface)
    #sys.stdout.flush()
    sniffing_data(iface)
    

if __name__ == '__main__':
    main()
