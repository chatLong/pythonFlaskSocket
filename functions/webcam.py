

class webcam:
    def get_webcam_video():
    global conn, addr
    data = b""
    payload_size = struct.calcsize(">L")
    print("payload_size: {}".format(payload_size))
    while True:
        while len(data) < payload_size:
            data += addr.recv(4096)
            if not data:
                cv2.destroyAllWindows()
                conn, addr = server_socket.accept()
                continue
        # receive image row data form client socket
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        while len(data) < msg_size:
            data += addr.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        # unpack image using pickle
        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        cv2.imshow('server', frame)
        cv2.waitKey(1)