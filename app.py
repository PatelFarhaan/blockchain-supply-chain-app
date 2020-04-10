from project import app, wallet, blockchain, port


if __name__ == '__main__':
    wallet = wallet(port)
    blockchain = blockchain(wallet.public_key, port)
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=True)