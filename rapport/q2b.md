<!-- Question 2 -->

<!-- (b) Combien y a-t-il de solutions possibles ? -->

Soit un sudoku binaire 3x3:
<table>
  <tr>
    <td style="border: 1px solid #000; padding: 8px;">x<sub>0</sub></td>
    <td style="border: 1px solid #000; padding: 8px;">x<sub>1</sub></td>
    <td style="border: 1px solid #000; padding: 8px;">x<sub>2</sub></td>
  </tr>
  <tr>
    <td style="border: 1px solid #000; padding: 8px;">x<sub>3</sub></td>
    <td style="border: 1px solid #000; padding: 8px;">x<sub>4</sub></td>
    <td style="border: 1px solid #000; padding: 8px;">x<sub>5</sub></td>
  </tr>
  <tr>
    <td style="border: 1px solid #000; padding: 8px;">x<sub>6</sub></td>
    <td style="border: 1px solid #000; padding: 8px;">x<sub>7</sub></td>
    <td style="border: 1px solid #000; padding: 8px;">x<sub>8</sub></td>
  </tr>
</table>

Il y a une contrainte par ligne<br>
Il y a une contrainte par colonne<br>
Il y a donc 6 contraintes<br>

Voici les 6 solutions possibles:

<div style="display:flex; justify-content: space-between;">
  <table>
    <tr>
      <td style="border: 1px solid #000; padding: 8px;">1</td>
      <td style="border: 1px solid #000; padding: 8px;">0</td>
      <td style="border: 1px solid #000; padding: 8px;">0</td>
    </tr>
    <tr>
      <td style="border: 1px solid #000; padding: 8px;">0</td>
      <td style="border: 1px solid #000; padding: 8px;">1</td>
      <td style="border: 1px solid #000; padding: 8px;">0</td>
    </tr>
    <tr>
      <td style="border: 1px solid #000; padding: 8px;">0</td>
      <td style="border: 1px solid #000; padding: 8px;">0</td>
      <td style="border: 1px solid #000; padding: 8px;">1</td>
    </tr>
    <tr><td colspan="3">|100010001></td></tr>
  </table>

  <table>
    <tr>
      <td style="border: 1px solid #000; padding: 8px;">1</td>
      <td style="border: 1px solid #000; padding: 8px;">0</td>
      <td style="border: 1px solid #000; padding: 8px;">0</td>
    </tr>
    <tr>
      <td style="border: 1px solid #000; padding: 8px;">0</td>
      <td style="border: 1px solid #000; padding: 8px;">0</td>
      <td style="border: 1px solid #000; padding: 8px;">1</td>
    </tr>
    <tr>
      <td style="border: 1px solid #000; padding: 8px;">0</td>
      <td style="border: 1px solid #000; padding: 8px;">1</td>
      <td style="border: 1px solid #000; padding: 8px;">0</td>
    </tr>
    <tr><td colspan="3">|100001010></td></tr>
  </table>
<table>
  <tr>
    <td style="border: 1px solid #000; padding: 8px;">0</td>
    <td style="border: 1px solid #000; padding: 8px;">1</td>
    <td style="border: 1px solid #000; padding: 8px;">0</td>
  </tr>
  <tr>
    <td style="border: 1px solid #000; padding: 8px;">1</td>
    <td style="border: 1px solid #000; padding: 8px;">0</td>
    <td style="border: 1px solid #000; padding: 8px;">0</td>
  </tr>
  <tr>
    <td style="border: 1px solid #000; padding: 8px;">0</td>
    <td style="border: 1px solid #000; padding: 8px;">0</td>
    <td style="border: 1px solid #000; padding: 8px;">1</td>
  </tr>
    <tr><td colspan="3">|010100001></td></tr>
</table>

<table>
  <tr>
    <td style="border: 1px solid #000; padding: 8px;">0</td>
    <td style="border: 1px solid #000; padding: 8px;">1</td>
    <td style="border: 1px solid #000; padding: 8px;">0</td>
  </tr>
  <tr>
    <td style="border: 1px solid #000; padding: 8px;">0</td>
    <td style="border: 1px solid #000; padding: 8px;">0</td>
    <td style="border: 1px solid #000; padding: 8px;">1</td>
  </tr>
  <tr>
    <td style="border: 1px solid #000; padding: 8px;">1</td>
    <td style="border: 1px solid #000; padding: 8px;">0</td>
    <td style="border: 1px solid #000; padding: 8px;">0</td>
  </tr>
  <tr><td colspan="3">|010001100></td></tr>
</table>

<table>
  <tr>
    <td style="border: 1px solid #000; padding: 8px;">0</td>
    <td style="border: 1px solid #000; padding: 8px;">0</td>
    <td style="border: 1px solid #000; padding: 8px;">1</td>
  </tr>
  <tr>
    <td style="border: 1px solid #000; padding: 8px;">1</td>
    <td style="border: 1px solid #000; padding: 8px;">0</td>
    <td style="border: 1px solid #000; padding: 8px;">0</td>
  </tr>
  <tr>
    <td style="border: 1px solid #000; padding: 8px;">0</td>
    <td style="border: 1px solid #000; padding: 8px;">1</td>
    <td style="border: 1px solid #000; padding: 8px;">0</td>
  </tr>
    <tr><td colspan="3">|001100010></td></tr>
</table>

<table>
  <tr>
    <td style="border: 1px solid #000; padding: 8px;">0</td>
    <td style="border: 1px solid #000; padding: 8px;">0</td>
    <td style="border: 1px solid #000; padding: 8px;">1</td>
  </tr>
  <tr>
    <td style="border: 1px solid #000; padding: 8px;">0</td>
    <td style="border: 1px solid #000; padding: 8px;">1</td>
    <td style="border: 1px solid #000; padding: 8px;">0</td>
  </tr>
  <tr>
    <td style="border: 1px solid #000; padding: 8px;">1</td>
    <td style="border: 1px solid #000; padding: 8px;">0</td>
    <td style="border: 1px solid #000; padding: 8px;">0</td>
  </tr>
  <tr><td colspan="3">|001010100></td></tr>
</table>

</div>
