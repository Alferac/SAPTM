*&---------------------------------------------------------------------*
*& Валидация ZCL_TM_V_CARRIER_MANDATORY (практикум, шаг 3)
*& Узел:     ROOT бизнес-объекта /SCMTMS/TOR
*& Вид:      consistency validation, блокирует сохранение
*& Триггеры: создание и изменение ROOT
*& Логика:   FO типа ZFO1 нельзя сохранить без перевозчика.
*& Сообщение ZTM/001: «Фрахтовый заказ &1: укажите перевозчика»
*&---------------------------------------------------------------------*
CLASS zcl_tm_v_carrier_mandatory DEFINITION
  PUBLIC FINAL CREATE PUBLIC
  INHERITING FROM /bobf/cl_lib_v_supercl_simple.

  PUBLIC SECTION.
    METHODS /bobf/if_frw_validation~execute REDEFINITION.

  PRIVATE SECTION.
    CONSTANTS gc_tor_type TYPE /scmtms/tor_type VALUE 'ZFO1'.
ENDCLASS.

CLASS zcl_tm_v_carrier_mandatory IMPLEMENTATION.

  METHOD /bobf/if_frw_validation~execute.
    DATA lt_root TYPE /scmtms/t_tor_root_k.

    " Валидация только читает: IO_MODIFY ей не передаётся
    io_read->retrieve(
      EXPORTING iv_node = is_ctx-node_key
                it_key  = it_key
      IMPORTING et_data = lt_root ).

    " CHECK: константа категории FO и имя поля перевозчика (TSPID)
    LOOP AT lt_root ASSIGNING FIELD-SYMBOL(<ls_root>)
         WHERE tor_cat  = /scmtms/if_tor_const=>sc_tor_category-active
           AND tor_type = gc_tor_type
           AND tspid    IS INITIAL.

      IF eo_message IS NOT BOUND.
        eo_message = /bobf/cl_frw_factory=>get_message( ).
      ENDIF.

      " Привязка к узлу и ключу: интерфейс подсветит нужный документ
      eo_message->add_message(
        is_msg  = VALUE #( msgty = 'E'
                           msgid = 'ZTM'
                           msgno = '001'
                           msgv1 = |{ <ls_root>-tor_id ALPHA = OUT }| )
        iv_node = is_ctx-node_key
        iv_key  = <ls_root>-key ).

      " Ключ в ET_FAILED_KEY — сигнал фреймворку, что проверка не пройдена
      INSERT VALUE #( key = <ls_root>-key ) INTO TABLE et_failed_key.
    ENDLOOP.
  ENDMETHOD.

ENDCLASS.
