import mysql.connector
import json

class DbClient:
    def __init__(self, configFile='config.json'):
        # Load database credentials from the config.json file
        self.config = self.loadConfig(configFile)

    def loadConfig(self, configFile):
        """Load configuration from JSON file"""
        with open(configFile, 'r') as file:
            return json.load(file)
    
    def connectToDB(self):
        """Establish a connection to the database"""
        return mysql.connector.connect(
            host=self.config["db"]["host"],
            port=self.config["db"]["port"], 
            user=self.config["db"]["user"],
            password=self.config["db"]["password"],
             database=self.config["db"]["database"],
            charset="utf8mb4",
            collation="utf8mb4_general_ci"
        )
    
    def executeQuery(self, query, data):
        """Helper function to execute an insert query and return success/failure response"""
        try:
            conn = self.connectToDB()
            cursor = conn.cursor()
            cursor.execute(query, data)
            conn.commit()
            response = {
                "status": "Success",
                "message": "Query executed successfully."
            }
        except mysql.connector.Error as err:
            response = {
                "status": "Failed",
                "message": f"Error: {err}"
            }
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
        return response

    def addCustomerData(self, customerData):
        """Add customer data to the customerData table"""
        query = """
        INSERT INTO customerData (name, customerType, email, phone, address, state, postcode, ABN)
        VALUES (%s, %s, %s, %s, %s, %s, %s,%s)
        """
        return self.executeQuery(query, (
            customerData['name'],
            customerData['customerType'],
            customerData['email'],
            customerData['phone'],
            customerData['address'],
            customerData['state'],
            customerData['postcode'],
            customerData['ABN']
        ))
    
    def getCustomerName(self):
        """Retrieve all customer IDs and names from the customerData table"""
        query = "SELECT customerID, name FROM customerData"
        
        try:
            conn = self.connectToDB()
            cursor = conn.cursor()
            cursor.execute(query)
            customerList = cursor.fetchall()  # Fetch all results
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            customerList = []  # Return an empty list on failure
        finally:
            cursor.close()
            conn.close()
        
        return customerList  # Returns a list of tuples [(id1, name1), (id2, name2), ...]

    def getCustomerIDByName(self, customerName):
        """Retrieve the customer ID based on the customer's name"""
        query = "SELECT customerID FROM customerData WHERE name = %s"
        
        try:
            conn = self.connectToDB()
            cursor = conn.cursor()
            cursor.execute(query, (customerName,))
            result = cursor.fetchone()
            customerID = result[0] if result else None
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            customerID = None
        finally:
            cursor.close()
            conn.close()
        
        return customerID

    def getCustomerDetails(self, customerID, name):
        """Retrieve customer details based on customer ID and name"""
        query = """
        SELECT customerID, customerType, name, address, state, postcode, phone, email, ABN 
        FROM customerData 
        WHERE customerID = %s AND name = %s
        """
        
        try:
            conn = self.connectToDB()
            cursor = conn.cursor()
            cursor.execute(query, (customerID, name))
            customerDetails = cursor.fetchone()  # Fetch only one result
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            customerDetails = None  # Return None on failure
        finally:
            cursor.close()
            conn.close()

        return customerDetails  # Returns a tuple or None if not found
    
    def addProductData(self, productData):
        """Insert new product into the productData table"""
        query = """
        INSERT INTO productData (productBarCode, name, price)
        VALUES (%s, %s, %s)
        """
        return self.executeQuery(query, (
            productData["productBarCode"],
            productData["name"],
            productData["price"]
        ))


    def getAllProducts(self):
        """Retrieve productID, name, and price from productData table"""
        query = """
            SELECT productID, name, price
            FROM productdata
            ORDER BY name
        """

        try:
            conn = self.connectToDB()
            cursor = conn.cursor()
            cursor.execute(query)
            products = cursor.fetchall()  # [(id, name, price), ...]
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            products = []
        finally:
            cursor.close()
            conn.close()

        return products

    
    def getPerDaySalesData(self):
        """Retrieve total sales grouped by date from the database."""
        query = """
        SELECT date, sales AS totalSales
        FROM perdaysale
        ORDER BY date DESC
        """
        try:
            conn = self.connectToDB()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
        except mysql.connector.Error:
            results = []
        finally:
            cursor.close()
            conn.close()
        return results
    

    def addSaleWithItems(self, saleData):
        """
        Add a sale with its items to the database.
        saleData: {
            "saleDate": date,
            "customerID": str or None,
            "paymentType": str,
            "note": str,
            "items": [
                {"name": str, "price": float, "quantity": int, "discount": float}
            ]
        }
        """
        response = {"status": "Failed", "message": "Unknown error"}

        if not saleData.get("items") or not saleData.get("paymentType"):
            response["message"] = "No products or payment type selected."
            return response

        try:
            conn = self.connectToDB()
            cursor = conn.cursor()

            # ------------------ Insert Sale ------------------
            customerID = saleData.get("customerID")
            if not customerID:
                customerID = None  # store NULL if no customer selected

            saleQuery = """
                INSERT INTO sales (saleDate, customerID, paymentType, note)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(saleQuery, (
                saleData["saleDate"],
                customerID,
                saleData["paymentType"],
                saleData.get("note")
            ))

            saleID = cursor.lastrowid  # get the auto-increment saleID

            # ------------------ Insert Sale Items ------------------
            itemQuery = """
                INSERT INTO saleItems (saleID, productName, cost, quantity)
                VALUES (%s, %s, %s, %s)
            """
            for item in saleData["items"]:
                # calculate final cost after discount
                price = float(item.get("price", 0))
                discount = float(item.get("discount", 0))
                cost = price * (1 - discount / 100)

                cursor.execute(itemQuery, (
                    saleID,
                    item["name"],
                    cost,
                    int(item.get("quantity", 1))
                ))

            # ------------------ Update Per-Day Sales ------------------
            totalSaleAmount = sum(
                float(item.get("price", 0)) * int(item.get("quantity", 1)) * (1 - float(item.get("discount", 0)) / 100)
                for item in saleData["items"]
            )

            # Check if record exists
            cursor.execute("SELECT totalSales FROM perDaySale WHERE saleDate = %s", (saleData["saleDate"],))
            result = cursor.fetchone()
            if result:
                updatedTotal = float(result[0]) + totalSaleAmount
                cursor.execute("UPDATE perDaySale SET totalSales = %s WHERE saleDate = %s", (updatedTotal, saleData["saleDate"]))
            else:
                cursor.execute("INSERT INTO perDaySale (saleDate, totalSales) VALUES (%s, %s)", (saleData["saleDate"], totalSaleAmount))

            conn.commit()
            response = {"status": "Success", "message": f"Sale saved successfully with Sale ID {saleID}"}

        except mysql.connector.Error as err:
            conn.rollback()
            response = {"status": "Failed", "message": f"Database error: {err}"}

        finally:
            cursor.close()
            conn.close()

        return response

    
    def getSalesByCustomerName(self, customerName):
        """Retrieve all sales records for a given customer name."""
        query = """
        SELECT date, customerAddress, customerPhone, productName, productType, colour, price, quantity, paymentType
        FROM salesData
        WHERE customerName = %s
        ORDER BY date DESC
        """

        try:
            conn = self.connectToDB()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (customerName,))
            sales = cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            sales = []
        finally:
            cursor.close()
            conn.close()

        return sales
    
    def getCreditSalesData(self):
        """Retrieve all sales transactions with payment type 'Credit'"""
        query = """
        SELECT date, customerName, customerAddress, customerPhone, productName, price, quantity
        FROM salesData WHERE paymentType = 'Credit'
        """
        try:
            conn = self.connectToDB()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
        except mysql.connector.Error:
            results = []
        finally:
            cursor.close()
            conn.close()
        return results


    def updatePaymentType(self, customerName):
        """Update payment type to 'Paid' for a given customer"""
        query = "UPDATE salesData SET paymentType = 'Paid' WHERE customerName = %s AND paymentType = 'Credit'"
        try:
            conn = self.connectToDB()
            cursor = conn.cursor()
            cursor.execute(query, (customerName,))
            conn.commit()
        except mysql.connector.Error:
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    # ------------------- Get Customer Sales History -------------------
    def getCustomerSalesHistory(self, customerID):
        query = """
            SELECT s.saleDate, si.productName, si.quantity, si.cost
            FROM sales s
            JOIN saleItems si ON s.saleID = si.saleID
            WHERE s.customerID = %s
            ORDER BY s.saleDate DESC
        """
        conn = self.connectToDB()
        cursor = conn.cursor()
        cursor.execute(query, (customerID,))
        return cursor.fetchall()




