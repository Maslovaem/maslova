"""
Создание ssh ключа

ssh-keygen -t ed25519 -C "your_email@example.com"
> Generating public/private ed25519 key pair.

> Enter a file in which to save the key (/Users/you/.ssh/id_ed25519): [Press enter]
Не использовать пароль при генерации ключа
> Enter passphrase (empty for no passphrase): [Press enter]
> Enter same passphrase again: [Press enter]

Добавление ключа в ssh-агент
Запустить в терминале shh-agent.
eval "$(ssh-agent -s)"
> Agent pid 59566
Добавить приватный ключ SSH в ssh-agent. 
$ ssh-add ~/.ssh/id_ed25519
В поле «Title» добавить описание нового ключа. 
Вставить ключ из буфера обмена в поле Key.

Клонирование репозитория
cd Имя_папки/
git clone ssh

"""
print("hello liza")

