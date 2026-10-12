# Шпаргалка

[← Программа](../README.md)

Одна страница, чтобы держать под рукой. Имена сверяйте с BOBF своей версии.

## Транзакции

| Транзакция | Назначение |
|---|---|
| `BOBF` | Модель бизнес-объекта |
| `/BOBF/TEST_UI` | Тестовый интерфейс BO: чтение, навигация, действия |
| `BOPF_EWB` | Расширение стандартных BO |
| `SE11` / `SE16` | Структуры, таблицы узлов, include расширения |
| `SE24` | Классы обработчиков и интерфейсы констант |
| `SE18` / `SE19` | BAdI TM, споты `/SCMTMS/*` |
| `SPRO` | Настройка: типы документов, условия, профили |
| `SPPFCADM` | Настройка PPF |
| `SLG1` | Журналы приложения |
| `SAT` / `ST05` | Анализ производительности и SQL |

## Бизнес-объекты

| BO | Документы | Интерфейс констант |
|---|---|---|
| `/SCMTMS/TRQ` | OTR, DTR, FWO, FWQ | `/SCMTMS/IF_TRQ_C` |
| `/SCMTMS/TOR` | FU, FO, FB, TU | `/SCMTMS/IF_TOR_C` |
| `/SCMTMS/SFIR` | Freight Settlement Document | ищите `/SCMTMS/IF_SFIR*` |
| `/SCMTMS/CFIR` | Forwarding Settlement Document | ищите `/SCMTMS/IF_CFIR*` |

Прикладные значения, например категории и статусы: `/SCMTMS/IF_TOR_CONST` и аналоги.

## TOR: узлы и таблицы

| Узел | Содержимое | Таблица |
|---|---|---|
| `ROOT` | Заголовок, `TOR_ID`, `TOR_CAT`, `TOR_TYPE`, статусы | `/SCMTMS/D_TORROT` |
| `ITEM_TR` | Позиции, иерархия транспорт → FU → товар | `/SCMTMS/D_TORITE` |
| `STOP` | Точки маршрута | `/SCMTMS/D_TORSTP` |
| `EXECUTION` | События исполнения | `/SCMTMS/D_TOREXE` |

Include расширения: `/SCMTMS/INCL_EEW_TOR_ROOT`, `/SCMTMS/INCL_EEW_TOR_ITEM` и аналоги для других узлов.

## BOPF API: снаружи

```abap
" Менеджеры
DATA(lo_srv) = /bobf/cl_tra_serv_mgr_factory=>get_service_manager( /scmtms/if_tor_c=>sc_bo_key ).
DATA(lo_tra) = /bobf/cl_tra_trans_mgr_factory=>get_transaction_manager( ).

" Чтение
lo_srv->convert_altern_key( iv_node_key, iv_altkey_key, it_key → et_key ).
lo_srv->query( iv_query_key, it_selection_parameters → et_key, et_data ).
lo_srv->retrieve( iv_node_key, it_key → et_data ).
lo_srv->retrieve_by_association( iv_node_key, it_key, iv_association, iv_fill_data → et_data, et_key_link ).

" Изменение
lo_srv->modify( it_modification → eo_change, eo_message ).
lo_srv->do_action( iv_act_key, it_key, is_parameters → eo_message, et_failed_key ).

" Сохранение
lo_tra->save( → ev_rejected, eo_message ).
lo_tra->cleanup( ).
```

## BOPF API: внутри обработчика

| Обработчик | Интерфейс | Базовый класс | Доступно |
|---|---|---|---|
| Детерминация | `/BOBF/IF_FRW_DETERMINATION` | `/BOBF/CL_LIB_D_SUPERCL_SIMPLE` | `io_read`, `io_modify` |
| Валидация | `/BOBF/IF_FRW_VALIDATION` | `/BOBF/CL_LIB_V_SUPERCL_SIMPLE` | `io_read` |
| Действие | `/BOBF/IF_FRW_ACTION` | `/BOBF/CL_LIB_A_SUPERCL_SIMPLE` | `io_read`, `io_modify`, `is_parameters` |

```abap
io_read->retrieve( iv_node, it_key → et_data ).
io_read->retrieve_by_association( iv_node, it_key, iv_association → et_data, et_key_link ).
io_modify->update( iv_node, iv_key, is_data, it_changed_fields ).
io_modify->create( iv_node, iv_key, is_data, iv_assoc_key, iv_source_node_key, iv_source_key ).
io_modify->delete( iv_node, iv_key ).
eo_message = /bobf/cl_frw_factory=>get_message( ).
```

## Пять правил

1. Пишите в BO только через BOPF API, никогда напрямую в таблицы.
2. В обработчиках нет `COMMIT`, `SELECT` по таблицам BO и вызовов Service Manager своего BO.
3. Первая строка обработчика на TOR — фильтр по `TOR_CAT` и `TOR_TYPE`.
4. Читайте пачкой по всем ключам, а не в цикле по одному.
5. Статусы меняйте действиями, а не обновлением полей.
