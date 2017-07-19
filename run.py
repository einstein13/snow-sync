#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from threading import active_count

from pipes.input import Input
from pipes.output import Output
from self_server.server import Server
from connection.link import Link
from commons.standard_objects import general_data

def main():
    input_queue = []
    output_queue = []

    input_object = Input(input_queue, output_queue, general_data)
    input_thread = input_object.run()
    output_object = Output(input_queue, output_queue, general_data)
    output_thread = output_object.run()

    server = Server(input_queue, output_queue, general_data)
    server_thread = server.run()

    while general_data['running']:
        sleep(3)

    # closing the server
    sleep(1)
    if active_count() != 1:
        output_object.print_data({'type': 'pretty_text', 'message': 'Hit any key to close'})
    else:
        output_object.print_data({'type': 'pretty_text', 'message': 'All thread closed'})

    # everything closed
    return

main ()
