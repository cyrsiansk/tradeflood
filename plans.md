### Ссылки

 * [Линковка](#линковка)
 * [Режимы работы](#режимы-работы)
 * [Предлагаемое решение](#предлагаемое-решение)
 * [Линковка In-Depth](#линковка-более-осмысленно)
 * [Proxy мысли](#что-нужно-определить-дальше)

# Планы

Всё, что будет описываться здесь - планы, которыми я обрисую намечающуюся работу.
Документ носит смешанный характер, так как содержать будет технические заметки, которые будут помогать мне не сбиваться с идей.


## TradeFlood - что это?

TradeFlood - это инструмент, который позволяют удобно и быстро вести работу с данными, предоставляемыми торговыми биржами.

Свечи, стаканы, индексы, всё, что придет на ум. Бинанс, битгет, форекс - придумай, внедри - заработает.

### ***Таким образом, столпом, на котором должен держаться TradeFlood, является расширяемость.***

## Линковка

Механизм расширения должен позволить расширять даже чужие модули, даже встроенные.
Этот механизм должен быть обеспечен через ***линковку*** - 
классу достаточно унаследоваться, чтобы он индексировался. 
Собираемые данные для инструмента (свечи, tf, стаканы, вообще всё, что хочется) - реализуется через линковку.
Тебе нужно создать класс, прописать связку с инструментном и прописать флоу обработки - сценарий, который будет отрабатывать каждый раз, собирая эти данные.

## Режимы работы

- Сбор данных актуальных
  - WebSocket
  - Callback
  - LongPoll
  
- Сбор данных исторических
  - REST API


Проблема:
* Сборы различаются, и, вероятно, на одной бирже можно получить стаканы сейчас, но только сейчас - никаких исторических данных.
* Таким образом, сбор по своей природе должен как-то различаться.

### Предлагаемое решение

Линкованные объекты - сборщики, которые определяют стратегию и упаковку.
Происходит запрос - происходит проход по всем возможно собираемым данным 
(не совсем ВСЕМ, а по всем, что требуются, зависит от определяемых действий, требуемых данных и так далее).

Процесс такой:
1) Приходит запрос на данные по активу
2) Перебираются все линкованные объекты, проверяется статус сбора по предикату в фабрике объекта
3) Составленный список объектов формирует стратегию сбора данных, определяющую список запросов
4) Сбор данных, что подразумевает запросы, результаты которых раздаются по фабрикам -> упаковка -> выдача


## Линковка (более осмысленно)

Линкование позволяет определить классы, связать их с различными сценариями.
Например, линкуется класс биржи Bitget, не требуя связок. Определяет логику.

* Класс "свеча" - модель. 

* BitgetCandleLinker - набор данных и процедур, определяющий сборку
объекта свечи. 
  > Линкуется определением метода LinkedData к Bitget классу.

* BitgetCandleLinker также определяет, что ему требуется запрос Bitget.getCandlesRequest, определяет действия над данными, которые будут он хочет


## Что нужно определить дальше?

Работа прокси в таком проекте не менее важна, чем его логика. В целом, можно организовать отдельный сервис, а может и контейнер (а значит и репозиторий <3) для работы с прокси.

Накидаю суть:

> Сервер-прокси, подключаешься, указывая в авторизации полезную нагрузку (тип запроса)
> 
> Каждый запрос в соответствии со своим типом распределяется по пулу прокси со своими ограничениями
> 
> Каждая группа настраиваемая - количество подключений ограничено, нагрузка - всё это замеряется
> 
> Отдельный сервис занимается отловом наисправных прокси, сообщает о них по настроенному callbackу, отдельным сервисом их простукивает 
>
> Также проблему этот прокси-сервис старается диагностировать - это какой-то сервер лёг, или прокси в целом, или может доступ к серверу прекратился от прокси
> 
> Таким образом, этот сервис позволяет добавлять и убирать прокси, отлавливать ошибки, совершать ротацию прокси с учетом распределения нагрузки по группам прокси (или в целом по прокси, два типа настройки)

В целом, это можно выделить в отдельный репозиторий, потому как подобная задача часто возникает, и обычно я отмахиваюсь от неё, добавлять random.choice(proxies)
Намного удобнее, когда можно указать в качестве прокси один контейнер, который сам очень круто совершает ротации, не так ли?

Таким образом, в процессе надо быстро разобраться с Golang и написать на нём этот сервис.


## Виденье структуры (спустя некоторое время, первая итерация обдумывания)

Проект - библиотека для сбора данных, поверх которой можно добавлять классы, изменять логику, увеличивать функционал.

В репозитории должно быть всё для запуска контейнера, который будет API-интерфейсом для работы с инструментами (сбор данных, веб-сокет соединения, callback-система).

Но это не исключает того, что библиотека должна быть такой, чтобы её можно было включить в проект.

Класс инструмента: Описывает взаимодействия (как правило, с внешним API). То, что задаёт сбор данных, должно использовать декоратор @request
Этот декоратор обеспечивает НЕвыполнение функции, а её добавление в стратегию сбора данных.

> ***Важно отметить, что скорее всего каждый отличающийся подход к сбору данных (вебсокеты, callback, longpoll) будет иметь свой источник, потому что формат работы и применения отличаются, похожи лишь форматы***

Класс Линкера: Описывает логику работы инструмента с датаклассом собираемых данных.
Линковкой привязывается к инструменту, в своем __call__ принимает класс инструмента, там он описывает путь данных, планируя сборку.

При инициализации инструмента происходит обход всех добавленных линкеров вызовом __call__.
Таким образом, собирается план сбора данных, который в дальнейшем будет вызываться.

При каждом вызове составляется склеенный граф (из разных цепочек вызовов), который создает цепь запросов без каких либо повторений

> Важно: если это невозможно нормально реализовать в языке, тогда стоит пытаться хотя бы собирать список нужных данных, формировать их базу, а затем происходит получение данных из собранной базы ресурсов, а не повторный запрос/склеивание источников)

> UPD: Только что реализовано. Он успешно берет, разделяет задачи, избавляется от повторений и работает по оптимальному пути.

## Обновленная структура (25 мая часть 2)

> Переименования:
> @request -> @turn system,
> Линковка -> Binding,
> Датакласс -> Model
> Прокси сервис на Go -> Proxyter,
> Инструмент -> Connector

### Библиотека:

Набор коннекторов на разные биржи (и на разные задачи - сбор данных, вебсокет соединения, callback-выдача).

Коннекторы работают через Прокси-схемы (класс, который контролирует работу с Proxyter, выдавая на даные типы запросов разные настройки распределения нагрузки)

Сбор данных от коннекторов происходит через забинженые классы, использующие методы коннекторов для генерации моделей.

Методы коннекторов, методы обработки данных в биндинге используют @turn_execution (конечные точки логики, в которых не ищется глубина дальше)

### Сервер

Сервер, упакованный в докер, который можно использовать как API-интерфейс для работы с коннекторами (сбор данных, веб-сокет соединения, callback-система).

Является частью библиотеки, но является второстепенным.

### Путь запроса

> Запрос -> Бинд -> Turn-схема -> Прокси-схема -> Proxyter -> Сервер -> Модель -> Ответ на запрос 