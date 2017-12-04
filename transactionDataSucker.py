from quadriga import QuadrigaClient
import datetime
import sqlite3

# Initialize the QuadrigaCX client                                                                       
client = QuadrigaClient(
        api_key = 'api_key',
        api_secret = 'api_secret',
        client_id = 'client_id',
        default_book = 'bch_cad'
        )

# Initialize SQLite database
conn = sqlite3.connect('quadrigaData.db')
c = conn.cursor()



def main():
        orderTimeStamp, orderBids, orderAsks = pullPublicOrders()
        writeListToSQLdb(orderTimeStamp, 0, orderBids)
        writeListToSQLdb(orderTimeStamp, 1, orderAsks)
        conn.close()
        
def pullPublicOrders():
        orderData = client.get_public_orders()
        orderTimeStamp = int(orderData['timestamp'])
        orderBids = [[float(bid[0]), float(bid[1])] for bid in orderData['bids']]
        orderAsks = [[float(ask[0]), float(ask[1])] for ask in orderData['asks']]

        return(orderTimeStamp, orderBids, orderAsks)
        #print(datetime.datetime.fromtimestamp(ordersTimeStamp))

        
# Writes an array of orders to the sql file
# orderTimeStamp: computer ticks
# orderType: 0 for bid, 1 for ask
# orders: Array of orders of the form [price, amount]
def writeListToSQLdb(orderTimeStamp, orderType, orders):

        transaction = [(orderTimeStamp, orderType, int(order[1]*(10**8)), int(order[0]*(10**2))) for order in orders]

        c.executemany("INSERT INTO transactionOrders (timeStamp, type, amount, price) VALUES (?,?,?,?);",(transaction))
        conn.commit()
        
        
main()
