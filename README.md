# cda2fhir-quality-measure
A repository containing an implementation for an algorithm to assess the quality of HL7 CDA to HL7 FHIR transformations.
*test_case_runner.py* runs the algorithm on a set of test cases and prints the results as a table. The test cases and expected reactions of the outputs are available below.

# Test case index
## case_1_1 
An exact transformation from CDA patient to FHIR patient

Expected: benchmark

## case_1_2
A transformation from CDA patient to FHIR practitioner

Expected: semantic similarity lowers, other stats remain the same or vary a little

## case_1_3
A transformation from CDA patient to FHIR patient with missing family name in output

Expected: semantic similarity remains the same, value similarity might lower slightly, length similarity lowers

## case_1_4
A transformation from CDA patient to FHIR patient with faulty classifier gender translation

Expected: semantic similarity remains the same, value similarity lowers, length similarity remains the same

## case_2_1
An exact transformation from CDA ANA section to a FHIR bundle

Expected: benchmark

## case_2_2
A transformation from CDA ANA section to a FHIR bundle with faulty resource choices on output

Expected: semantic similarity lowers, other stats remain the same or vary a little

## case_2_3
A transformation from CDA ANA section to a FHIR bundle with untransformed codes and dates

Expected: semantic similarity remains the same, value similarity might lowers slightly, length similarity lowers

## case_2_4
A transformation from CDA ANA section to a FHIR bundle with faulty classifier translation

Expected: semantic similarity remains the same, value similarity lowers, length similarity remains the same
