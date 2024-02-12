Project Description:
The aim of this project is to create a program that generates template designs and testbench Verilog modules. The program will handle the following tasks:
•	Module Design: Generate a file with a name matching the module and write the template module design code into it.
•	Testbench Design: Generate a file with a name matching the module and append "Testbench" to the filename. Write the testbench module code into this file.

Information File Description:
In this project, I took inputs and outputs from a text file, only enter the number of inputs and outputs and name of inputs with number of bits, same for output. 
Here the file you have fill to generate a module and module_Tb from python code:
You can fill this file with number of inputs and outputs you want with just their names and width. As shown the first col in (Design.txt file) is the name and second col is the width. 
Just for clk and reset signal, you’ve to write clock or rest in any form (upper or lower case) in third col. 
The empty lines just for to clarify every section, and theses empty lines will be handled in the code.
