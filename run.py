#!/usr/local/bin/python

import requests
import json
import time

BLOCKCYPHER_API_ROOT = 'https://api.blockcypher.com/v1/bcy/test'
NEW_TXN_API = BLOCKCYPHER_API_ROOT + '/txs/new'
SEND_TXN_API = BLOCKCYPHER_API_ROOT + '/txs/send'
ADDRS_API = BLOCKCYPHER_API_ROOT + '/addrs'
BALANCE_API = BLOCKCYPHER_API_ROOT + '/addrs/%s/balance'

OFFSITE_ADDRS = 'C1rGdt7QEPGiwPMFhNKNhHmyoWpa5X92pn'

def new_wallet():
  """
  Requests the generation of a new key pair and address from Blockcypher.
  Throws a BCAPIException if the request fails.
  """
  r = requests.post(ADDRS_API, data={})
  check_status_code(r, 201)

  return r.json()

def addrs_balance_url(address):
  """
  Generates the URL to check the balance of a particular `address`.
  """
  return BALANCE_API % address

def get_balance(address):
  """
  Requests the balance for `address` from Blockcypher.  Throws a BCAPIException
  if the request fails.
  """
  url = addrs_balance_url(address)
  r = requests.get(url)
  check_status_code(r, 200)

  return r.json()['balance']


def create_txn(in_addr, amount):
  """
  Creates a new multi sig txn to the vending machine's wallet given the input
  address and amount.  
  """
  data = {
    'inputs':  [{
      'addresses': [in_addr]
    }],
    'outputs': [{
      'addresses':   OFFSITE_ADDRS,
      'value':       amount
    }]
  }

  res = requests.post(NEW_TXN_API, data=json.dumps(data))
  check_status_code(res, 201)

  return res.json()

def send_mult_sig_txn(txn_json):
  """
  Send the txn to blockcypher api to be processed.
  """
  res = requests.post(SEND_TXN_API, data=txn_json) 
  check_status_code(res, 201)

  return res.json()

class BCAPIException(RuntimeError):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

def check_status_code(response, code, route):
  if response.status_code != code:
    raise BCAPIException('Request failed with code ' + str(r.status_code))

if __name__ == "__main__":
  wallet = None
  balance = 0
  product = None
  txn == None

  while True:
    if wallet == None:
      try:
        wallet = new_wallet()
      except BCAPIException as e:
        print 'Failed to generate new wallet:', e
        time.sleep(5)
        break

    address = wallet['address']
    # show address

    try: 
      balance = get_balance(address)
    except BCAPIException as e:
      print 'Failed to check balance for', (address + ':'), e
      time.sleep(5)
      break

    # display BTC value received

    if product == None:
      try:
        # get product code/value
      except VendingIOException as e:
        print 'Failed to receive product from vending machine:', e
        time.sleep(1)
        break

    if product['value'] < balance:
      # account needs more funding
      product = None
      break

    # Dispense product

    # Send balance to offsite wallet
    if txn == None
      try:
        txn = create_txn(address, balance)
      except BCAPIException as e:
        print 'Failed to create txn:', e
        time.sleep(5)
        break

    private = wallet['private']
    # Sign transaction

    try:
      send_txn(txn)
    except BCAPIException as e:
      print 'Failed to send txn:', e
      time.sleep(5)
      break

    wallet = None
    balance = 0
    product = None
    txn = None



