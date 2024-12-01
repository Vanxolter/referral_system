```sudo apt-get install pgbouncer```


Для создания пароля в userlist нужно прописать команду 
```echo -n "referral_systemreferral_system" | md5sum```

Где "referral_system" - название базы данных + пароль

после чего вписываем хэш в userlist = md5 + хэш

