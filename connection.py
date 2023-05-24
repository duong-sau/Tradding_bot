def register_connections(binance_thread, logic_thread, socket_thread, main_view):

    # order
    main_view.open_order_signal.connect(logic_thread.open_order)
    logic_thread.open_order_signal.connect(binance_thread.open_order)

    # socket
    socket_thread.order_trigger_signal.connect(binance_thread.handle_socket_event)

    # pnl
    binance_thread.update_pnl_signal.connect(main_view.update_pnl)
