import re
reserved_names_file = "reserved_names.txt"
with open(reserved_names_file , 'r') as reserved_file:
    reserved_names = [name.strip() for name in reserved_file.readlines()]

def is_valid_name(name, reserved_names):
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_$]*$', name):
        print(f"Error: {name} is an invalid name. Name can only begin with a character or '_'.")
        return False
    elif name in reserved_names:
        print(f"Error: {name} is an invalid name. Name can't be a reserved word.")
        return False
    return True
def get_non_empty_input(prompt):
    while True:
        user_input = input(prompt)
        if user_input.strip():
            return user_input.strip()
        
def get_valid_alwaysall_input():
    while True:
        alwaysall = get_non_empty_input("You have combinational always? Enter y for Yes or n for No: ")
        if alwaysall.lower() in ['y', 'n','yes','no']:
            return alwaysall.lower()
        else:
            print("Error: Invalid input. Please enter 'y' or 'n'.")
module_name = input("Enter the name of your Verilog module: ")

while not is_valid_name(module_name,reserved_names):
    module_name = input("Re-enter the name of your Verilog module: ")

filename =get_non_empty_input("Enter the filename with input and output information: ")
alwaysall=get_valid_alwaysall_input()

always_clk = False
always_rst = False
CLKName=""
RSTName=""

with open(filename, 'r') as file:
    lines = file.readlines()
lines = [line.strip() for line in lines if line.strip()]
used_names = set()

input_info = []
num_inputs = int(lines[0].split()[0])
for i in range(1, num_inputs + 1):
    input_data = lines[i].split()
    input_name = input_data[0]
    input_width_bits = int(input_data[1])
    
    # Check if "clock" or "rest" is present in the third column
    if len(input_data) > 2 and "clock" in lines[i].split()[2].lower():
        always_clk = True
        CLKName = input_name

    if len(input_data) > 2 and "rest" in lines[i].split()[2].lower():
        always_rst = True
        RSTName = input_name
        
    while not is_valid_name(input_name, reserved_names) or input_name in used_names:
        input_name = input(f"Re-enter the input name {input_name}: ")
    used_names.add(input_name)
    input_info.append((input_name, input_width_bits))
    replaced_line = lines[i].replace(lines[i].split()[0], input_name)
    if replaced_line != lines[i]:
        replacement_occurred = True
        print("Your information file is updated by corrected inputs")
    lines[i] = replaced_line


output_info = []
num_outputs = int(lines[num_inputs + 1].split()[0])

for i in range(num_inputs + 2, num_inputs + num_outputs + 2):
    output_data = lines[i].split()
    output_name = output_data[0]
    output_width_bits = int(output_data[1])
    
    while not is_valid_name(output_name, reserved_names) or output_name in used_names:
        output_name = input(f"Re-enter the output name {output_name}: ")
    used_names.add(output_name)

    output_info.append((output_name, output_width_bits))
    replaced_line = lines[i].replace(lines[i].split()[0], output_name)
    if replaced_line != lines[i]:
        replacement_occurred = True
        print("Your information file is updated by corrected outputs")
    lines[i] = replaced_line

counter=0
with open(filename, 'w') as file:
    file.write('\n'.join(lines))
    
with open(module_name+".v", 'w') as file_save:
    file_save.write(f"module {module_name} (\n")

    for input_name, input_width_bits in input_info:

        if input_width_bits == 1:
            file_save.write(f"  input {input_name},\n")
        else:
            file_save.write(f"  input [{input_width_bits - 1}:0] {input_name},\n")

    for output_name, output_width_bits in output_info:
        if always_clk or always_rst or (alwaysall=='y' or alwaysall=='yes'):
            if output_width_bits == 1:
                counter+=1
                file_save.write(f"  output reg  {output_name}")
                if(counter != num_outputs):
                    file_save.write(", \n")
            else:
                counter+=1
                file_save.write(f"  output reg [{output_width_bits - 1}:0] {output_name}")
                if(counter != num_outputs):
                    file_save.write(", \n")
        else:
            if output_width_bits == 1:
                counter+=1
                file_save.write(f"  output  {output_name}")
                if(counter != num_outputs):
                    file_save.write(", \n")
            else:
                counter+=1
                file_save.write(f"  output [{output_width_bits - 1}:0] {output_name}")
                if(counter != num_outputs):
                    file_save.write(", \n")
            

    file_save.write(");\n\n\n")

    if always_clk and always_rst:
        clkedge=input("Do you want\n1-Positive edge clock\n2-Negative edge clock\nEnter your choice:")
        if clkedge=='1':
            file_save.write(f"  always @(posedge {CLKName} or negedge {RSTName})\n   begin\n\n   \n\n")
            file_save.write(f"     if(!{RSTName})\n\n       begin\n\n\n       end\n\n     else\n\n       begin\n\n\n       end\n\n\n   end\n\n")
        else:
            file_save.write(f"  always @(negedge {CLKName} or negedge {RSTName})\n   begin\n\n   \n\n")
            file_save.write("     if(!rst)\n\n       begin\n\n\n       end\n\n     else\n\n       begin\n\n\n       end\n\n\n   end\n\n")
    elif always_clk:
        clkedge=input("Do you want\n1-Positive edge clock\n2-Negative edge clock\nEnter your choice:")
        if clkedge=='1':
            file_save.write(f"  always @(posedge {CLKName} )\n   begin\n\n   end\n\n")
        else:
            file_save.write(f"  always @(negedge {CLKName} )\n   begin\n\n   end\n\n")
    elif always_rst:
        file_save.write(f"  always @(negedge {RSTName})\n   begin\n\n   end\n\n")
   # file_save.write("   end\n\n")
    if alwaysall=='y' or alwaysall=='yes':
        file_save.write("  always @(*)\n   begin\n\n   end\n\n\n")

    file_save.write("endmodule\n")


Testbench=module_name+'_TB'+".v"
counterTb=0
with open(Testbench, 'w') as file_handler:
    file_handler.write("`timescale 1ns / 1ps\t\t//The default time scale\n\n")
    
    file_handler.write(f"module {module_name}_TB;\n \n")
    
    for input_name, input_width_bits in input_info:
        if input_width_bits == 1:
            file_handler.write(f"  reg {input_name}_TB;\n")
        else:
            file_handler.write(f"  reg [{input_width_bits - 1}:0] {input_name}_TB;\n")
    for output_name, output_width_bits in output_info:
        if output_width_bits == 1:
            file_handler.write(f"  wire  {output_name}_TB;\n")
        else:
            file_handler.write(f"  wire [{output_width_bits - 1}:0] {output_name}_TB;\n")
    if always_clk:
        clkperiod=int(input("Enter the value of clk period:"))
        if clkperiod %2==0:
            file_handler.write(f"\n  localparam t={clkperiod//2}; \n")
        else:
            file_handler.write(f"  localparam t={clkperiod/2}; \n")
    file_handler.write(f"\n\n  {module_name}  {module_name}_TB ( \n")
    for input_name,input_width_bits in input_info:
        file_handler.write(f"   .{input_name} ({input_name}_TB),\n")
    for output_name, output_width_bits in output_info:
        counterTb+=1
        file_handler.write(f"   .{output_name} ({output_name}_TB)")
        if(counterTb != num_outputs):
           file_handler.write(",\n")
    file_handler.write(");\n\n\n")

    file_handler.write("  initial\n\n   begin\n\n")
    if always_clk:
        file_handler.write(f"    forever #t {CLKName}_TB=~{CLKName}_TB\n\n")
    file_handler.write("   end\n\n")
    file_handler.write("endmodule")
    
print(f"Verilog module declaration for {module_name} has been saved to {module_name}.")
print(f"Verilog Test Bench module declaration for {module_name}_TB has been saved to {module_name}_TB.")