<?php

class Sudoku {

    private $initialTable;    // a tabla kezdeti allapota
    private $table;           // ebbe keszul a megoldas

    public function __construct($_table){
        $this->table = $_table;
        $this->initialTable = $_table;
    }

    /**
     * Ellenorzi hogy adott koordinataju ertekbol van-e megegy az OSZLOPban
     * @return boolean
     */
    private function checkColumn($y, $x){
        $found = false;
        for($i=0; $i<9; $i++){
            if($i == $x) continue;
            if( $this->table[$x][$y] == $this->table[$i][$y] ){
                $found = true;
            }
        }
    return  $found;
    }

    /**
     * Ellenorzi hogy adott koordinataju ertekbol van-e megegy a SORban
     * @return boolean
     */
    private function checkRow($y, $x){
        $found = false;
        for($i=0; $i<9; $i++){
            if($i == $y) continue;
            if( $this->table[$x][$y] == $this->table[$x][$i] ){
                $found = true;
            }
        }
    return $found;
    }

    /**
     * Ellenorzi hogy adott koordinataju ertekbol van-e megegy a 3x3 CELLAban
     * @return boolean
     */
    private function checkCell($x, $y){
        // 3x3as cella koordinatainak meghatarozasa ami tartalmazza a kijelolt elemet
        if($x < 3){ $fromX = 0; $toX = 3; }
        else if(3 <= $x && $x < 6) { $fromX = 3; $toX = 6; }
        else if($x >= 6){ $fromX = 6; $toX = 9; }

        if($y < 3){ $fromY = 0; $toY = 3; }
        else if(3 <= $y && $y < 6) { $fromY = 3; $toY = 6; }
        else if($y >= 6){ $fromY = 6; $toY = 9; }

        // 3x3as cella atnezese
        $found = false;
        for($j=$fromY; $j<$toY; $j++){
            for($i=$fromX; $i<$toX; $i++){
                if($i==$x && $j==$y) continue;
                if($this->table[$j][$i] == $this->table[$y][$x]) $found = true;
            }
        }
    return $found;
    }

    /**
     * Ellenorzi hogy az alap kitoltes valid-e
     * @return boolean
     */
    private function isValidTable(){
        for($j=0; $j<9; $j++){
            for($i=0; $i<9; $i++){
                if($this->table[$j][$i] == 0) continue;
                if($this->checkRow($i,$j) || $this->checkColumn($i,$j) || $this->checkCell($i,$j)){
                    return false;
                }
            }
        }
        return true;
    }

    /**
     * Megoldja a sudoku feladvanyt backtrack algoritmussal
     *
     * Ket for ciklussal atnezi a 2D tombot es ha szabalytalan lepest talal
     * akkor visszalep elozo cellara a ciklusvaltozo csokkentesevel.
     *
     * @see https://en.wikipedia.org/wiki/Sudoku_solving_algorithms
     * @return array(array)
     */
    public function solve(){
        $this->table = $this->initialTable;

        // ha az alap kitoltes serti a szabalyokat el sem kezdjuk
        if( !$this->isValidTable() ){ return false; }

        $backtrackHappened = false;
        for($j=0; $j<9; $j++){
            for($i=0; $i<9; $backtrackHappened?$backtrackHappened=false:$i++){

                // csak a szabad helyeket toltom ki
                if($this->initialTable[$j][$i] == 0){
                    
                    // cella ertek novelese
                    $this->table[$j][$i]++;

                    // szabalyok ellenorzese
                    while($this->checkRow($i,$j) || $this->checkColumn($i,$j) || $this->checkCell($i,$j)){
                        
                        // ha elertem a 9-et akkor backtrack
                        if($this->table[$j][$i] == 9){

                            // backtrack = vissza olyan cellara ami nem 9 es szabad cella
                            while($this->table[$j][$i] == 9 || $this->initialTable[$j][$i] != 0 ){

                                // a 9 erteku cellakat kinullazom
                                if($this->table[$j][$i] == 9 && $this->initialTable[$j][$i] == 0){
                                    $this->table[$j][$i] = 0;
                                }

                                // maga a backtrack
                                $i--;                    // oszlop valtas
                                if($i<0){ $i=8; $j--;}   // sor valtas ha elfogyott az oszlop
                                $backtrackHappened = true;

                                // ha backtrack kifut a tombbol akkor nem megoldhato
                                if($j<0) return false;
                            }
                            break;

                        // ha nem kell backtrack akkor cella noveles
                        } else {
                            $this->table[$j][$i]++;
                        }
                    }
                }
            }
        }

    return $this->table;
    }

    /**
     * Olvashatoan kinyomtatja a tablazatot a 3x3-as cellakat is elkulonitve
     */
    public function print($solve = false){
        
        if($solve && $this->solve() == false){
            echo "<p>No solution.</p>"; return;
        }

        if($solve) { 
            echo "<p>Solution:</p>"; 
        }

        for($x=0; $x<9; $x++){
            for($y=0; $y<9; $y++){
                if($this->initialTable[$x][$y] != 0) echo "<span style='background-color:lightgreen'>";
                echo $this->table[$x][$y] . " ";
                if($this->initialTable[$x][$y] != 0 ) echo "</span>";
                if($y == 2 || $y == 5) echo " <font color='red'>|</font> ";
            }
            echo "<br>";
            if($x == 2 || $x == 5) echo "<font color='red'>-----------------------</font><br>";
        }
    }
}

$example = [
    [0, 0, 4, 0, 9, 0, 0, 0, 0],
    [0, 6, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 0, 5, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 1, 0, 3, 4, 0, 0],
    [3, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 9, 0, 4, 0, 0, 0],
];

$zero = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
];

$onlynine = [
    [9, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
];

$worlds_hardest = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0],
];

$sequence = [
    [9, 8, 7, 6, 5, 4, 3, 2, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
];

$diagonal_sequence = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 4, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 5, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 6, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 7, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 9],
];

$diagonal_sequence2 = [
    [9, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 7, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 6, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 5, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 4, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 3, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1],
];

$x = [
    [9, 0, 0, 0, 0, 0, 0, 0, 6],
    [0, 8, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 7, 0, 0, 0, 9, 0, 0],
    [0, 0, 0, 6, 0, 8, 0, 0, 0],
    [0, 0, 0, 0, 5, 0, 0, 0, 0],
    [0, 0, 0, 7, 0, 4, 0, 0, 0],
    [0, 0, 4, 0, 0, 0, 3, 0, 0],
    [0, 3, 0, 0, 0, 0, 0, 2, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 1],
];

$most_clues = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 2, 0, 3, 4, 5, 6, 7],
    [0, 3, 4, 5, 0, 6, 1, 8, 2],
    [0, 0, 1, 0, 5, 8, 2, 0, 6],
    [0, 0, 8, 6, 0, 0, 0, 0, 1],
    [0, 2, 0, 0, 0, 7, 0, 5, 0],
    [0, 0, 3, 7, 0, 5, 0, 2, 8],
    [0, 8, 0, 0, 6, 0, 7, 0, 0],
    [2, 0, 7, 0, 8, 3, 6, 1, 5],
];

$everycell = [
    [9, 0, 0, 8, 0, 0, 7, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6, 0, 0, 5, 0, 0, 4, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 0, 0, 2, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
];

$invalid = [
    [9, 9, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
];

$unsolvable = [
    [5, 1, 6, 8, 4, 9, 7, 3, 2],
    [3, 0, 7, 6, 0, 5, 0, 0, 0],
    [8, 0, 9, 7, 0, 0, 0, 6, 5],
    [1, 3, 5, 0, 6, 0, 9, 0, 7],
    [4, 7, 2, 5, 9, 1, 0, 0, 6],
    [9, 6, 8, 3, 7, 0, 0, 5, 0],
    [2, 5, 3, 1, 8, 6, 0, 7, 4],
    [6, 8, 4, 2, 0, 7, 5, 0, 0],
    [7, 9, 1, 0, 5, 0, 6, 0, 8],
];



echo "<h2>Example</h2>";
$sudoku = new Sudoku($example);
$sudoku->print();
$sudoku->print(true);

echo "<h2>Full zero table</h2>";
$sudoku = new Sudoku($zero);
$sudoku->print();
$sudoku->print(true);

echo "<h2>Only 9</h2>";
$sudoku = new Sudoku($onlynine);
$sudoku->print();
$sudoku->print(true);

echo "<h2>World's hardest table</h2>";
$sudoku = new Sudoku($worlds_hardest);
$sudoku->print();
$sudoku->print(true);

echo "<h2>Sequence</h2>";
$sudoku = new Sudoku($sequence);
$sudoku->print();
$sudoku->print(true);

echo "<h2>Diagonal sequence</h2>";
$sudoku = new Sudoku($diagonal_sequence);
$sudoku->print();
$sudoku->print(true);

echo "<h2>Diagonal sequence 2</h2>";
$sudoku = new Sudoku($diagonal_sequence2);
$sudoku->print();
$sudoku->print(true);

echo "<h2>X</h2>";
$sudoku = new Sudoku($x);
$sudoku->print();
$sudoku->print(true);

echo "<h2>Most clues, only 1 solution</h2>";
echo "<small><a href='https://en.wikipedia.org/wiki/Mathematics_of_Sudoku#Maximum_number_of_givens'>https://en.wikipedia.org/wiki/Mathematics_of_Sudoku#Maximum_number_of_givens</a></small>";
$sudoku = new Sudoku($most_clues);
$sudoku->print();
$sudoku->print(true);

echo "<h2>In every cell</h2>";
$sudoku = new Sudoku($everycell);
$sudoku->print();
$sudoku->print(true);


echo "<h2>Invalid</h2>";
$sudoku = new Sudoku($invalid);
$sudoku->print();
$sudoku->print(true);

echo "<h2>Unsolvable</h2>";
$sudoku = new Sudoku($unsolvable);
$sudoku->print();
$sudoku->print(true);
