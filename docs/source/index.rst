DataclassDb
=========================

DataclassDb is a lightweight sqlite3 ORM for dataclasses.
Column constraints, such as ``PRIMARY KEY`` can be defined using plain text in an Annotated field:

.. tab:: DataclassDb

   .. code-block:: python

      from dataclasses import dataclass, field
      from typing import Annotated
      from dataclassdb import DataclassDb

      @dataclass
      class Example:
         id: Annotated[int, "PRIMARY KEY"]
         username: Annotated[str, "UNIQUE"]
         friends: list[str] = field(default_factory = list)

   Write to Database

   .. code-block:: python

      with DataclassDb(Example, "example.db") as db:
         db.insert(Example(0, "user_0", ["user_b", "user_d"]))
         db.insert_many(list_of_example)
         
   Read from Database

   .. code-block:: python

      with DataclassDb(Example, "example.db") as db:
         db.get(0) # Get from specific key
         db.get(0, select_fields = ["friends"]) # Get specific field from object 
         db.peek() # Get last inserted

.. tab:: QueryBuilder

   .. code-block:: python

      from dataclassdb import QueryBuilder

      qb = QueryBuilder()
      qb.SELECT("*").FROM(Example).WHERE("id").eq(0)



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   generated/dataclassdb


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`


   
