# EletromagArrays

  Esta coleção de códigos permite calcular o campo elétrico resultante de um arranjo arbitrário de antenas. É possível parametrizar a posição,
orientação, e corrente de alimentação de alimentação de cada antena do arranjo individualmente, e então calcular o campo elétrico resultante do
arranjo levando em consideração o fator de arranjo, rotação do campo elétrico, fase e magnitude da alimentação de cada antena.

  Parametrizando as antenas, é possível ainda criar rotinas de otimização numérica para que o arranjo atenda os requisitos do sistema, dimensionando
a diretividade e ângulos de abertura do arranjo conforme desejado.

  As antenas utilizadas neste trabalho foram projetadas e simuladas no ANSYS HFSS. Seus campos elétricos foram exportados individualmente em arquivos
.csv, e importados para o código desenvolvido. Com as antenas projetadas, foram criados e simulados arranjos no HFSS. Os campos elétricos resultantes
destes arranjos foram exportados e importados como uma antena no código, e então os mesmos arranjos foram recriados no código utilizando as antenas
individualmente. Assim, estes arranjos foram utilizados para validar o código desenvolvido.

  Os códigos calculam os campos elétricos na região de campos distantes, ou seja, assumindo que o ponto de observação do campo elétrico está a uma
distância $r$ muito maior das antenas que o comprimento de onda $\lambda_0$ das ondas eletromagnéticas emitidas. Assume-se que as ondas eletromagnéticas
se propagam no espaço livre.

For creating, simulating and optimizing antenna arrays from Antennas developed in HFSS. EletromagArrays is a collection of Octave and Python scripts capable of modeling arbitrary antenna arrays and computing their resultant electromagnetic fields from the individual electric field of each antenna composing the array. It is suitable for systems excited with constant frequencies (Harmonic Regime) working on the far-field (Fraunhofer field) of the array and when each antenna is positioned in the far fields of all neighbors antennas, so that inducted currents on other antennas can be ignored. Each antenna is modeled as a point-like source of electromagnetic fields. The resultant fields are calculated from the array factor resulting from the translation and rotation of each antenna. The position, orientation and current magnitude and phase can be parametrized individually.

Trabalho de conclusão de curso 2 de engenharia aeroespacial, Universidade de Brasília, campus do Gama.
Autor: Vítor Lima Aguirra
