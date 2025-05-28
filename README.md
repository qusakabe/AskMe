## Результаты тестирования
### Отдача статического документа напрямую через nginx
```
Server Software:        nginx/1.24.0
Server Hostname:        localhost
Server Port:            80

Document Path:          /static/sample.html
Document Length:        3753 bytes

Concurrency Level:      100
Time taken for tests:   0.427 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      4091000 bytes
HTML transferred:       3753000 bytes
Requests per second:    2341.43 [#/sec] (mean)
Time per request:       42.709 [ms] (mean)
Time per request:       0.427 [ms] (mean, across all concurrent requests)
Transfer rate:          9354.27 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    1   1.4      0       7
Processing:    10   39   6.6     40      78
Waiting:        7   39   6.6     40      78
Total:         14   40   6.1     40      80

Percentage of the requests served within a certain time (ms)
  50%     40
  66%     41
  75%     41
  80%     42
  90%     43
  95%     44
  98%     59
  99%     71
 100%     80 (longest request)
```
### Отдача статического документа напрямую через gunicorn
```
Server Software:        gunicorn
Server Hostname:        localhost
Server Port:            8082

Document Path:          /
Document Length:        3753 bytes

Concurrency Level:      100
Time taken for tests:   1.924 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      3871000 bytes
HTML transferred:       3753000 bytes
Requests per second:    519.66 [#/sec] (mean)
Time per request:       192.433 [ms] (mean)
Time per request:       1.924 [ms] (mean, across all concurrent requests)
Transfer rate:          1964.46 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    1   2.2      0      11
Processing:     5  181  33.7    190     210
Waiting:        5  181  33.8    190     210
Total:         16  182  31.7    190     210

Percentage of the requests served within a certain time (ms)
  50%    190
  66%    194
  75%    195
  80%    196
  90%    201
  95%    207
  98%    209
  99%    209
 100%    210 (longest request)
```
### Отдача динамического доукмента через gunicorn
```
Server Software:        gunicorn
Server Hostname:        127.0.0.1
Server Port:            8082

Document Path:          /login/
Document Length:        3257 bytes

Concurrency Level:      50
Time taken for tests:   104.927 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      3688000 bytes
HTML transferred:       3257000 bytes
Requests per second:    9.53 [#/sec] (mean)
Time per request:       5246.350 [ms] (mean)
Time per request:       104.927 [ms] (mean, across all concurrent requests)
Transfer rate:          34.32 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.2      0       2
Processing:   235 5088 871.6   5313    6457
Waiting:      235 5088 871.6   5312    6457
Total:        237 5088 871.5   5313    6457

Percentage of the requests served within a certain time (ms)
  50%   5313
  66%   5430
  75%   5507
  80%   5542
  90%   5669
  95%   6039
  98%   6321
  99%   6372
 100%   6457 (longest request)
```
### Отдача динамического документа через проксирование запроса с nginx на gunicorn
```
Server Software:        nginx/1.24.0
Server Hostname:        localhost
Server Port:            80

Document Path:          /login/
Document Length:        3257 bytes

Concurrency Level:      100
Time taken for tests:   105.972 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      3701000 bytes
HTML transferred:       3257000 bytes
Requests per second:    9.44 [#/sec] (mean)
Time per request:       10597.187 [ms] (mean)
Time per request:       105.972 [ms] (mean, across all concurrent requests)
Transfer rate:          34.11 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    1   2.5      0      13
Processing:   249 10026 2074.4  10724   12973
Waiting:      249 10026 2074.5  10724   12973
Total:        262 10027 2072.7  10724   12974

Percentage of the requests served within a certain time (ms)
  50%  10724
  66%  10915
  75%  10985
  80%  11078
  90%  11758
  95%  12330
  98%  12640
  99%  12838
 100%  12974 (longest request)
```
### Отдача динамического документа при кешировании ответа на nginx
```
Server Software:        nginx/1.24.0
Server Hostname:        localhost
Server Port:            80

Document Path:          /login/
Document Length:        3257 bytes

Concurrency Level:      100
Time taken for tests:   2.668 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      3722001 bytes
HTML transferred:       3257000 bytes
Requests per second:    374.84 [#/sec] (mean)
Time per request:       266.780 [ms] (mean)
Time per request:       2.668 [ms] (mean, across all concurrent requests)
Transfer rate:          1362.46 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        3   13   6.6     11      42
Processing:     1   17  75.6     14    2399
Waiting:        1   12  74.4      8    2357
Total:         13   30  75.6     28    2405

Percentage of the requests served within a certain time (ms)
  50%     28
  66%     30
  75%     31
  80%     32
  90%     34
  95%     39
  98%     53
  99%     54
 100%   2405 (longest request)
```

## Насколько быстрее отдается статика по сравнению с WSGI?
Он ускоряет работу примерно в 6 раз
## Во сколько раз ускоряет работу proxy_cache?
Судя по тестам примерно в 40 раз