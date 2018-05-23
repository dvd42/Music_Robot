from __future__ import print_function
import socket
import common
import os

def start(ip,port):
	max_petitions = 1

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((ip,port))
	print("Started server on " + ip + ":" + str(port))
	s.listen(max_petitions)
	print("Listening")
	while True:
		conn, cl_address = s.accept()
		print(str(cl_address) + " connected\n")

		params = common.recv_file(conn)
		print("Recived: " + str(params))
		decoded_params = common.decode(params, True)
		print("Data decoded: " + str(decoded_params))
		generate_song(decoded_params)



def generate_song(decoded_params):
    os.system("performance_rnn_generate --config='multiconditioned_performance_with_dynamics' --bundle_file=/home/diego/Desktop/Universidad/3ro/2do_Semestre/rlp/Music_Robot/magenta/multiconditioned_performance_with_dynamics.mag --output_dir=./outRNN --num_outputs=1 --num_steps=" + str(decoded_params['time']) + " --pitch_class_histogram=\"" + str(decoded_params['scale']) + "\" --notes_per_second=" + str(decoded_params['tempo']))
    os.system("ls | grep .mid >> log.txt")
    os.system("timidity ./outRNN/song.mid -Ow -o - | lame - -b 64 ./outRNN/song.mp3")
    os.system("scp ./outRNN/song.mp3 pi@192.168.43.167:rlp/magenta_audio/song.mp3")

if __name__ == "__main__":
	start("192.168.43.86",8089)





