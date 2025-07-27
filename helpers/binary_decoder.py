catagory =['Form, Structure, and Sense', 'Boundaries', 'Inferences', 'Command of Evidence', 'Central Ideas and Details', 'Transitions', 'Rhetorical Synthesis', 'Words in Context', 'Text Structure and Purpose', 'Cross-Text Connections', 'Circles', 'Right triangles and trigonometry', 'Lines, angles, and triangles', 'Area and volume', 'Evaluating statistical claims: Observational studies and experiments', 'Inference from sample statistics and margin of error', 'Probability and conditional probability', 'Two-variable data: Models and scatterplots', 'One-variable data: Distributions and measures of center and spread', 'Percentages', 'Ratios, rates, proportional relationships, and units', 'Nonlinear functions', 'Nonlinear equations in one variable and systems of equations in two variables', 'Equivalent expressions', 'Linear inequalities in one or two variables', 'Systems of two linear equations in two variables', 'Linear equations in two variables', 'Linear functions', 'Linear equations in one variable']

def decode(encoded):
    returned = []
    binary_digits = '0'*(29-len(bin(int(encoded))[2:])) + bin(int(encoded))[2:] # → '00000000000000000000000000000100'
    print(binary_digits)
    for index, i in enumerate(binary_digits):
        if i == '1':
            returned.append(catagory[index])
    return returned