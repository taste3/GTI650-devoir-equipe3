<!-- Question 1 -->

<!-- (a) Expliquez comment on peut encoder la contrainte sur la première ligne à l’aide d’un circuit avec un qubit ancillaire. -->

Soit un sudoku binaire 2x2:
<table>
  <tr>
    <td style="border: 1px solid #000; padding: 8px;">x<sub>0</sub></td>
    <td style="border: 1px solid #000; padding: 8px;">x<sub>1</sub></td>
  </tr>
  <tr>
    <td style="border: 1px solid #000; padding: 8px;">x<sub>2</sub></td>
    <td style="border: 1px solid #000; padding: 8px;">x<sub>3</sub></td>
  </tr>
</table>

La contrainte sur la première ligne est qu'il doit y avoir un seul 1 dans une des deux cases de la ligne.

Voici comment on peut exprimer cette contrainte:
<br>
x<sub>0</sub> ⊕ x<sub>1</sub> = 1

Le circuit qui fait l'équivalent de la porte XOR et qui encode la contrainte sur la première ligne est celui-ci:
<br>
<div style="text-align:center;">
  <img src="../images/circuit_q1a.jpg" width="200"/>
</div>