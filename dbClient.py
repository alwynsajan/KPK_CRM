import mysql.connector
import json
from datetime import datetime

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
        query = """
            INSERT INTO customerData
            (name, customerType, email, phone, address, state, postcode, ABN)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            customerData["name"],
            customerData["customerType"],
            customerData["email"],
            customerData["phone"],
            customerData["address"],
            customerData["state"],
            customerData["postcode"],
            customerData["ABN"]
        )

        try:
            conn = self.connectToDB()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()

            response = {
                "status": "Success",
                "message": "Customer added successfully.",
                "customerID": cursor.lastrowid
            }

        except mysql.connector.Error as err:
            conn.rollback()
            response = {
                "status": "Failed",
                "message": f"Error: {err}"
            }

        finally:
            cursor.close()
            conn.close()

        return response

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
    
    # ------------------- Add Sale with Items -------------------
    def addSaleWithItems(self, saleData):
        response = {
            "status": "Failed",
            "message": "Unknown error",
            "saleID": None
        }

        if not saleData.get("items") or not saleData.get("paymentType"):
            response["message"] = "No products or payment type selected."
            return response

        try:
            conn = self.connectToDB()
            cursor = conn.cursor()

            # ------------------ Insert Sale ------------------
            customerID = saleData.get("customerID") or None

            saleQuery = """
                INSERT INTO sales (saleDateTime, customerID, paymentType, note)
                VALUES (%s, %s, %s, %s)
            """

            saleDateTime = saleData.get("saleDateTime") or datetime.now()

            cursor.execute(
                saleQuery,
                (
                    saleDateTime,
                    customerID,
                    saleData["paymentType"],
                    saleData.get("note")
                )
            )

            saleID = cursor.lastrowid

            # ------------------ Insert Sale Items ------------------
            itemQuery = """
                INSERT INTO saleItems (saleID, productName, cost, quantity)
                VALUES (%s, %s, %s, %s)
            """

            totalSaleAmount = 0

            for item in saleData["items"]:
                price = float(item.get("price", 0))
                discount = float(item.get("discount", 0))
                quantity = int(item.get("quantity", 1))

                cost = price * (1 - discount / 100)
                totalSaleAmount += cost * quantity

                cursor.execute(
                    itemQuery,
                    (saleID, item["name"], cost, quantity)
                )

            # ------------------ Update Per-Day Sales ------------------
            saleDateOnly = saleDateTime.date()

            cursor.execute(
                "SELECT totalSales FROM perDaySale WHERE saleDate = %s",
                (saleDateOnly,)
            )
            result = cursor.fetchone()

            if result:
                cursor.execute(
                    "UPDATE perDaySale SET totalSales = %s WHERE saleDate = %s",
                    (float(result[0]) + totalSaleAmount, saleDateOnly)
                )
            else:
                cursor.execute(
                    "INSERT INTO perDaySale (saleDate, totalSales) VALUES (%s, %s)",
                    (saleDateOnly, totalSaleAmount)
                )

            conn.commit()

            response = {
                "status": "Success",
                "message": "Sale saved successfully",
                "saleID": saleID
            }

        except mysql.connector.Error as err:
            conn.rollback()
            response = {
                "status": "Failed",
                "message": f"Database error: {err}",
                "saleID": None
            }

        finally:
            cursor.close()
            conn.close()

        return response

    
    def getSalesByCustomerID(self, customerID):
        """Retrieve all sales records for a given customer name."""
        query = """
        SELECT date, customerAddress, customerPhone, productName, productType, colour, price, quantity, paymentType
        FROM sales
        WHERE customerID = %s
        ORDER BY date DESC
        """

        try:
            conn = self.connectToDB()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (customerID,))
            sales = cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            sales = []
        finally:
            cursor.close()
            conn.close()

        return sales
    
    def getCreditSales(self):
        """Get all sales with payment type 'Credit'"""
        query = """
        SELECT 
            s.saleID,
            s.saleDateTime,
            s.paymentType,
            s.note,
            c.name as customerName,
            c.address as customerAddress,
            c.phone as customerPhone,
            c.state as customerState,
            c.postcode as customerPostcode,
            c.email as customerEmail
        FROM sales s
        LEFT JOIN customerData c ON s.customerID = c.customerID
        WHERE s.paymentType = 'Credit'
        ORDER BY s.saleDateTime DESC, s.saleID DESC
        """
        
        try:
            conn = self.connectToDB()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            sales = cursor.fetchall()
            
            # Get items for each sale
            for sale in sales:
                saleID = sale['saleID']
                items_query = """
                SELECT productName, cost, quantity
                FROM saleItems
                WHERE saleID = %s
                """
                cursor.execute(items_query, (saleID,))
                sale['items'] = cursor.fetchall()
                
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            sales = []
        finally:
            cursor.close()
            conn.close()
        
        return sales

    def updatePaymentType(self, saleID, paymentType):
        """Update payment type for a sale"""
        query = """
        UPDATE sales
        SET paymentType = %s
        WHERE saleID = %s
        """
        
        try:
            conn = self.connectToDB()
            cursor = conn.cursor()
            cursor.execute(query, (paymentType, saleID))
            conn.commit()
            
            if cursor.rowcount > 0:
                return {"status": "Success", "message": "Payment type updated successfully"}
            else:
                return {"status": "Error", "message": "No sale found with given ID"}
                
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return {"status": "Error", "message": f"Database error: {err}"}
        finally:
            cursor.close()
            conn.close()

    # ------------------- Get Customer Sales History -------------------
    def getCustomerSalesHistory(self, customerID):
        query = """
            SELECT s.saleDateTime, si.productName, si.quantity, si.cost
            FROM sales s
            JOIN saleItems si ON s.saleID = si.saleID
            WHERE s.customerID = %s
            ORDER BY s.saleDateTime DESC
        """

        try:
            conn = self.connectToDB()
            cursor = conn.cursor()
            cursor.execute(query, (customerID,))
            result = cursor.fetchall()

        except mysql.connector.Error as err:
            result = []
            print(f"Database Error: {err}")

        finally:
            cursor.close()
            conn.close()

        return result

    # ------------------- Update Customer Details -------------------
    def updateCustomerData(self, customerID, customerData):
        """Update customer details in the database."""
        query = """
        UPDATE customerData 
        SET name = %s, 
            customerType = %s,
            email = %s,
            phone = %s,
            address = %s,
            state = %s,
            postcode = %s,
            ABN = %s
        WHERE customerID = %s
        """
        
        try:
            conn = self.connectToDB()
            cursor = conn.cursor()
            
            cursor.execute(query, (
                customerData.get("name", ""),
                customerData.get("customerType", ""),
                customerData.get("email", ""),
                customerData.get("phone", ""),
                customerData.get("address", ""),
                customerData.get("state", ""),
                customerData.get("postcode", ""),
                customerData.get("ABN", ""),
                customerID
            ))
            
            conn.commit()
            
            if cursor.rowcount > 0:
                return {"status": "Success", "message": "Customer updated successfully"}
            else:
                return {"status": "Error", "message": "No customer found with given ID"}
                
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return {"status": "Error", "message": f"Database error: {err}"}
        finally:
            cursor.close()
            conn.close()

    # ------------------- Delete Customer -------------------
    def deleteCustomerData(self, customerID):
        """Delete customer from database."""
        query = "DELETE FROM customerData WHERE customerID = %s"
        
        try:
            conn = self.connectToDB()
            cursor = conn.cursor()
            cursor.execute(query, (customerID,))
            conn.commit()
            
            if cursor.rowcount > 0:
                return {"status": "Success", "message": "Customer deleted successfully"}
            else:
                return {"status": "Error", "message": "No customer found with given ID"}
                
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return {"status": "Error", "message": f"Database error: {err}"}
        finally:
            cursor.close()
            conn.close()



