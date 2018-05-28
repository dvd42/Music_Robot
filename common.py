import socket
import cPickle as pickle
import sys
import struct


def decode(data,is_serialized):
	if is_serialized:
		f = open("tmp.pickle","w")
		f.write(data)
		f.close()

		with open('tmp.pickle', 'rb') as f:
			data = pickle.load(f)

		return data
	
	else:
		with open('new_song.mid', 'w') as f:
			f.write(data)
			f.close()
	
		return data

def serialize(data):
	with open('serialized.pickle', 'wb') as f:
		pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)

	return "serialized.pickle"

def file2string(file):
	f = open(file,"rb")
	return f.read()	

def recv_file(s):
	print "recv_file"
	acc_data_size=0;
	data=[];
	data_size=sys.maxint

	partial_data='';
	data_size_data=""
	buffer_data=8192
	while acc_data_size < data_size:
		partial_data=s.recv(buffer_data)
		if not data:
			if len(partial_data)>4 or len(data_size_data) > 4:
				data_size_data+=partial_data
				data_size=struct.unpack('>i', data_size_data[:4])[0]
				buffer_data=data_size
				if buffer_data>524288:buffer_data=524288
				data.append(data_size_data[4:])
			else:
				data_size_data+=partial_data
		else:
			data.append(partial_data)
		acc_data_size=sum([len(i) for i in data ])
	return ''.join(data)

def send_file(s,data,close,serialize_data):
	print "send_file"
	if serialize_data:
		file = serialize(data)
		data = file2string(file)
	s.sendall(struct.pack('>i', len(data))+data)
	if close:
		s.close()
	else:
		return s

