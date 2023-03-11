def register_connections(binance_thread, logic_thread, main_view):
    # price
    binance_thread.update_price_signal.connect(logic_thread.update_price)
    logic_thread.update_price_signal.connect(main_view.update_price)

    # order
    main_view.open_order_signal.connect(logic_thread.open_order)
    logic_thread.open_order_signal.connect(binance_thread.open_order)

    # symbol
    binance_thread.set_symbols_signal.connect(main_view.set_symbols)

    # symbol
    main_view.update_symbol_signal.connect(binance_thread.update_symbol)
