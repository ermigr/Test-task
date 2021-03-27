<?php
$data = [
    'question' => ['почему', 'как', 'зачем', 'столько'],
    'animals' => [
        'birds' => [
            [
                'name' => 'грачи',
            ],
            [
                'name' => 'воробьи',
            ],
        ],
        'others' => [
            [
                ['name' => 'кошки'],
                ['name' => 'рыбы'],
                ['name' => 'собаки'],
            ],
        ],
    ],
    'parts' => [
        'hands' => 'рук',
        'feathers' => 'перьев',
        'eyes' => 'глаз',
    ],
];

/* почему грачи не кошки и зачем им столько перьев */
echo $data['question'][0];
echo ' ';
echo $data['animals']['birds'][0]['name'];
echo ' ';
echo array_search ('грачи', $data['animals']['birds'][0])[0];
echo substr($data['question'][0],6,2);
echo ' ';
echo $data['animals']['others'][0][0]['name'];
echo ' ';
echo substr($data['animals']['birds'][0]['name'],8,2);
echo ' ';
echo $data['question'][2];
echo ' ';
echo substr($data['animals']['birds'][0]['name'],8,2);
echo substr($data['question'][2],8,2);
echo ' ';
echo $data['question'][3];
echo ' ';
echo $key[0];
echo $data['parts']['feathers'];