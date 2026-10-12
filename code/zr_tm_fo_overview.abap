*&---------------------------------------------------------------------*
*& Отчёт ZR_TM_FO_OVERVIEW
*& Учебный пример к дню 3: чтение документа TOR через BOPF API.
*& Только чтение: MODIFY и SAVE не вызываются.
*& Места, которые нужно сверить с BOBF вашей системы, помечены CHECK.
*&---------------------------------------------------------------------*
REPORT zr_tm_fo_overview.

PARAMETERS p_torid TYPE /scmtms/tor_id OBLIGATORY.

CLASS lcl_app DEFINITION FINAL.
  PUBLIC SECTION.
    METHODS run IMPORTING iv_tor_id TYPE /scmtms/tor_id.

  PRIVATE SECTION.
    DATA mo_srv  TYPE REF TO /bobf/if_tra_service_manager.
    DATA mt_text TYPE string_table.

    METHODS collect_messages
      IMPORTING io_message TYPE REF TO /bobf/if_frw_message.
ENDCLASS.

CLASS lcl_app IMPLEMENTATION.

  METHOD run.
    DATA lt_tor_id   TYPE STANDARD TABLE OF /scmtms/tor_id WITH EMPTY KEY.
    DATA lt_root_key TYPE /bobf/t_frw_key.
    DATA lt_root     TYPE /scmtms/t_tor_root_k.
    DATA lt_item     TYPE /scmtms/t_tor_item_tr_k.
    DATA lt_stop     TYPE /scmtms/t_tor_stop_k.           " CHECK: тип таблицы узла STOP
    DATA lo_message  TYPE REF TO /bobf/if_frw_message.

    " 0. Service Manager бизнес-объекта /SCMTMS/TOR
    mo_srv = /bobf/cl_tra_serv_mgr_factory=>get_service_manager(
               /scmtms/if_tor_c=>sc_bo_key ).

    " 1. Номер документа -> технический ключ (GUID)
    lt_tor_id = VALUE #( ( |{ iv_tor_id ALPHA = IN }| ) ).

    mo_srv->convert_altern_key(
      EXPORTING iv_node_key   = /scmtms/if_tor_c=>sc_node-root
                iv_altkey_key = /scmtms/if_tor_c=>sc_alternative_key-root-tor_id
                it_key        = lt_tor_id
      IMPORTING eo_message    = lo_message
                et_key        = lt_root_key ).
    collect_messages( lo_message ).
    DELETE lt_root_key WHERE key IS INITIAL.

    IF lt_root_key IS INITIAL.
      MESSAGE |Документ { iv_tor_id ALPHA = OUT } не найден| TYPE 'S' DISPLAY LIKE 'E'.
      RETURN.
    ENDIF.

    " 2. Заголовок: узел ROOT
    mo_srv->retrieve(
      EXPORTING iv_node_key = /scmtms/if_tor_c=>sc_node-root
                it_key      = lt_root_key
      IMPORTING eo_message  = lo_message
                et_data     = lt_root ).
    collect_messages( lo_message ).

    " 3. Позиции: ассоциация ROOT -> ITEM_TR
    mo_srv->retrieve_by_association(
      EXPORTING iv_node_key    = /scmtms/if_tor_c=>sc_node-root
                it_key         = lt_root_key
                iv_association = /scmtms/if_tor_c=>sc_association-root-item_tr
                iv_fill_data   = abap_true
      IMPORTING eo_message     = lo_message
                et_data        = lt_item ).
    collect_messages( lo_message ).

    " 4. Стопы: ассоциация ROOT -> STOP
    mo_srv->retrieve_by_association(
      EXPORTING iv_node_key    = /scmtms/if_tor_c=>sc_node-root
                it_key         = lt_root_key
                iv_association = /scmtms/if_tor_c=>sc_association-root-stop   " CHECK
                iv_fill_data   = abap_true
      IMPORTING eo_message     = lo_message
                et_data        = lt_stop ).
    collect_messages( lo_message ).

    " 5. Вывод
    DATA(lo_out) = cl_demo_output=>new( ).
    LOOP AT lt_root ASSIGNING FIELD-SYMBOL(<ls_root>).
      lo_out->write_text( |Документ { <ls_root>-tor_id ALPHA = OUT }: | &&
                          |категория { <ls_root>-tor_cat }, тип { <ls_root>-tor_type }| ).
    ENDLOOP.
    lo_out->next_section( |Позиции ITEM_TR: { lines( lt_item ) }| ).
    lo_out->write_data( lt_item ).
    lo_out->next_section( |Стопы STOP: { lines( lt_stop ) }| ).
    lo_out->write_data( lt_stop ).
    IF mt_text IS NOT INITIAL.
      lo_out->next_section( 'Сообщения BOPF' ).
      lo_out->write_data( mt_text ).
    ENDIF.
    lo_out->display( ).
  ENDMETHOD.

  METHOD collect_messages.
    " Сообщения BOPF — объекты исключений с текстом, узлом и ключом строки
    CHECK io_message IS BOUND.
    io_message->get_messages( IMPORTING et_message = DATA(lt_msg) ).
    LOOP AT lt_msg ASSIGNING FIELD-SYMBOL(<ls_msg>).
      APPEND <ls_msg>-message->get_text( ) TO mt_text.
    ENDLOOP.
  ENDMETHOD.

ENDCLASS.

START-OF-SELECTION.
  NEW lcl_app( )->run( p_torid ).
