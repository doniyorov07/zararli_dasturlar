<?php
// Papka nomi
$papka_nomi = "../python";


$dir_iterator = new RecursiveDirectoryIterator($papka_nomi);
$iterator = new RecursiveIteratorIterator($dir_iterator, RecursiveIteratorIterator::SELF_FIRST);
$boyut = 0;

foreach ($iterator as $dosya) {
    if ($dosya->isFile()) {
        $boyut += $dosya->getSize();
        $qator_soni = count(file($dosya));
        echo "Fayl: " . $dosya->getFilename() . ", Hajmi: " . $dosya->getSize() . " bayt, Qatorlar soni: " . $qator_soni . "\n";
    }
}

echo "Papka hajmi: " . $boyut . " bayt\n";
?>
