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
        params = common.recv_file(conn)
        decoded_params = common.decode(params, True)
        generate_song(decoded_params)


def generate_song(decoded_params):

        os.system("performance_rnn_generate --config='multiconditioned_performance_with_dynamics' --bundle_file=/home/diego/Desktop/Universidad/3ro/2do_Semestre/rlp/Music_Robot/magenta/multiconditioned_performance_with_dynamics.mag --output_dir=./magenta/outRNN --num_outputs=1 --num_steps=" + str(decoded_params['time']) + " --pitch_class_histogram=\"" + str(decoded_params['scale']) + "\" --notes_per_second=" + str(decoded_params['tempo']))
        os.system("ls magenta/outRNN | grep .mid >> magenta/outRNN/log.txt")
        os.system("./magenta/outRNN/get_file.sh")

if __name__ == "__main__":
	start("192.168.43.86",8089)





