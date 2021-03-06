# -*- coding: Windows-1252 -*-
# -*- coding: cp1252 -*-
# -*- coding: utf-8 -*-
"""
Created on Tue May 21 17:28:54 2019

Clase encargada de  realizar la conexión con la base de datos de neo4j

Referencia:
    <> https://neo4j-rest-client.readthedocs.io/en/latest/info.html
    <> https://neo4j.com/developer/python/
    <> PanMat. (2018). How to Access Relationship value from 
            returned results. Extraído de: https://community.neo4j.com/t/how-to-access-relationship-value-from-returned-results/1316
    
@author: Pablo Sao
"""
from neo4j import GraphDatabase

class Connection:
    
    def __init__(self, uri="", user="", password=""):
        try:
            self._driver = GraphDatabase.driver(uri, auth=(user, password))
        except ImportError:
            raise Exception('No se ha encontrado el módulo: neo4j')
        except Exception as e:
            raise Exception('Error: {0}'.format(str(e)))
            
    
    def close(self):
        self._driver.close()

    def createDB(self,query):
        with self._driver.session() as session:
            # Eliminamos base de datos si existe
            session.write_transaction(self.deleteDB)
            session.write_transaction(self.ejecutar,query)


    def ejecuteQuery(self,query):        
        greeting = {}
        
        with self._driver.session() as session:
            greeting = session.write_transaction(self.ejecutar, query)
            

        return greeting



    @staticmethod
    def deleteDB(tx):
        try:
            tx.run('MATCH (n) DETACH DELETE n')
        except:
            return False
        return True

    @staticmethod
    def ejecutar(tx,script):
        return tx.run(script)
