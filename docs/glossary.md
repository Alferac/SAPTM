# Глоссарий

[← Программа](../README.md)

## Бизнес-понятия TM

| Термин | Сокр. | Объяснение |
|---|---|---|
| Business Partner | BP | Контрагент: перевозчик, клиент, отправитель, получатель |
| Carrier | TSP | Перевозчик. В технических именах — Transportation Service Provider |
| Charge Calculation | TCC | Расчёт стоимости перевозки по ставкам соглашений |
| Delivery-Based Transportation Requirement | DTR | Потребность в перевозке из поставки |
| Document Flow | — | Цепочка связанных документов: спрос, FU, FO, расчёты |
| Forwarding Agreement | FWA | Договор с клиентом экспедитора: ставки продажи |
| Forwarding Order | FWO | Заказ клиента на перевозку у экспедитора |
| Forwarding Quotation | FWQ | Предложение клиенту до заказа |
| Forwarding Settlement Document | FWSD | Счёт клиенту, передаётся в SD |
| Freight Agreement | FA | Договор с перевозчиком: ставки закупки |
| Freight Booking | FB | Бронь мест у морского или авиаперевозчика |
| Freight Order | FO | Рейс: транспорт, маршрут, груз |
| Freight Settlement Document | FSD | Расчёт с перевозчиком, передаётся в MM |
| Freight Unit | FU | Неделимая единица планирования |
| Freight Unit Building Rule | FUBR | Правило разбиения спроса на FU |
| Logistics Service Provider | LSP | Экспедитор или логистический оператор |
| Location | — | Точка сети: завод, склад, клиент, порт, хаб |
| Means of Transport | MTR | Вид транспорта: фура, вагон, контейнеровоз |
| Order-Based Transportation Requirement | OTR | Потребность в перевозке из заказа |
| Resource | — | Конкретная единица транспорта: машина, трейлер |
| Shipper | — | Грузоотправитель, перевозит собственный товар |
| Stage | — | Этап маршрута между двумя соседними стопами |
| Stop | — | Точка маршрута с локацией и временем |
| Tendering | — | Запрос предложений у перевозчиков |
| Transportation Cockpit | — | Рабочее место планировщика |
| Transportation Lane | — | Допустимое направление: откуда, куда, каким транспортом |
| Transportation Unit | TU | Трейлер, вагон или контейнер как отдельная единица планирования |
| Transportation Zone | — | Группа локаций или географический регион |
| Vehicle Scheduling and Routing | VSR | Оптимизатор планирования |

## Технические понятия

| Термин | Объяснение |
|---|---|
| Action | Операция бизнес-объекта, вызывается через `DO_ACTION` |
| Alternative key | Бизнес-ключ, например номер документа, с преобразованием в GUID |
| Association | Навигация между узлами одного или разных BO |
| BOPF | Business Object Processing Framework: фреймворк бизнес-объектов SAP |
| Buffer | Данные BO в памяти до сохранения |
| Business Object, BO | Модель документа: дерево узлов с поведением |
| CFIR | Customer Freight Invoice Request, бизнес-объект FWSD |
| Combined structure | Структура `…_K`: технические ключи плюс все поля узла |
| Consistency validation | Проверка данных после изменения и при сохранении |
| Constants interface | Интерфейс `…_C` с GUID узлов, связей, действий и запросов |
| Delegated node | Узел, модель которого взята из другого объекта |
| Determination | Обработчик, который вычисляет и меняет данные |
| EEW include | Include расширения узла для своих полей: `/SCMTMS/INCL_EEW_*` |
| FBI | Интеграция FPM с BOPF: интерфейс строится по модели BO |
| FPM | Floorplan Manager: каркас интерфейса на Web Dynpro ABAP |
| Node | Узел BO, хранится в своей таблице |
| PPF | Post Processing Framework: действия после сохранения, печать, отправка |
| Query | Поиск экземпляров узла по критериям |
| Service Manager | Фасад BO для чтения и изменения |
| SFIR | Supplier Freight Invoice Request, бизнес-объект FSD |
| TOR | Transportation Order, бизнес-объект FU, FO, FB и TU |
| `TOR_CAT` | Категория TOR: FU, FO, FB или TU |
| `TOR_TYPE` | Тип документа TOR из настройки |
| Transaction Manager | Сохранение и откат изменений всех BO |
| TRQ | Transportation Request, бизнес-объект OTR, DTR, FWO и FWQ |
| Validation | Обработчик, который проверяет данные и сообщает об ошибках |
