<?php
//Запрос на создание таблицы
$create="CREATE TABLE `test` (
  `ID` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `NAME` text NOT NULL,
  `DATA_INSERT` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
)";
//Запрос на внесение записей
$insert="INSERT INTO `test` (`ID`, `NAME`, `DATA_INSERT`) VALUES
(null, 'Ivanov', default),
(null, 'Petrov', default),
(null, 'Sidorov', default);";

//Создаем функцию для работы с таблицей
function sql($query) {
	define('SERVER','localhost');
	define('LOGIN','root');
	define('PASS','root');
	define('DB','lesson');
	$connect=mysqli_connect(SERVER,LOGIN,PASS,DB);    //Подключение к базе данных

	return mysqli_query($connect,$query);
}
//Создаем таблицу, вносим записи
sql($create);
sql($insert);

//Выводим данные
//Вариант №1-вывод по названию поля
$arResult=[];
$query='select*from test';
$sql=sql($query);
//Получение ассоциативного массива из MySQL
while ($res=mysqli_fetch_assoc($sql)) {
	foreach($res as $key=>$item) {
		if (!$arResult[$key]) {
			$arResult[$key]=[];
		}
		array_push($arResult[$key],$item);
	}
}
print_r($arResult);    //Ctrl-U для наглядности

//Вариант №2-вывод по записям
$arResult=[];
$query='select*from test';
$sql=sql($query);
while ($res=mysqli_fetch_assoc($sql)) {
	$arResultItem=[];
	foreach($res as $key=>$item) {
		$arResultItem[$key]=$item;
	}
	array_push($arResult,$arResultItem);
}
print_r($arResult);
?>