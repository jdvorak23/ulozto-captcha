<?php
/*ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);*/

require("UrlParser.php");
$url = new UrlParser($_SERVER['REQUEST_URI']);

if ($url->request === 'captcha') {
    $data = file_get_contents('php://input');
    if($data){
        $data = json_decode($data);
        $src = $data[0]->src;
        $pos = strpos($src, ";base64,");
        $base = base64_decode(substr($src, $pos + 8));
        file_put_contents('./captcha.jpg', $base, FILE_USE_INCLUDE_PATH);
        $settings = parse_ini_file(__DIR__ . "/settings.ini", false, INI_SCANNER_RAW);
        $result = shell_exec($settings['python'] . " " . __DIR__ . "/captcha.py");
	    $result = file_get_contents('./result.txt');
        echo trim($result);
    }
}elseif($url->request === 'wrong-captcha'){
    $data = file_get_contents('php://input');
    if ($data){
        $data = json_decode($data);
        $name = $data[0];
        $fileName = __DIR__ . "/images/" . $name . ".jpg";
        if(file_exists($fileName))
            unlink($fileName);
    }
}

