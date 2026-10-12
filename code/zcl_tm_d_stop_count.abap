*&---------------------------------------------------------------------*
*& Детерминация ZCL_TM_D_STOP_COUNT (практикум, шаг 2)
*& Узел:     ROOT бизнес-объекта /SCMTMS/TOR
*& Триггеры: создание, изменение, удаление узла STOP
*& Момент:   before save
*& Логика:   для FO типа ZFO1 записать количество стопов в ZZ_STOP_COUNT.
*&           Поле ZZ_STOP_COUNT добавлено append-структурой
*&           к /SCMTMS/INCL_EEW_TOR_ROOT (шаг 1).
*&---------------------------------------------------------------------*
CLASS zcl_tm_d_stop_count DEFINITION
  PUBLIC FINAL CREATE PUBLIC
  INHERITING FROM /bobf/cl_lib_d_supercl_simple.

  PUBLIC SECTION.
    METHODS /bobf/if_frw_determination~execute REDEFINITION.

  PRIVATE SECTION.
    " В реальном проекте тип берут из Z-таблицы настроек, а не из константы
    CONSTANTS gc_tor_type TYPE /scmtms/tor_type VALUE 'ZFO1'.
ENDCLASS.

CLASS zcl_tm_d_stop_count IMPLEMENTATION.

  METHOD /bobf/if_frw_determination~execute.
    DATA lt_root      TYPE /scmtms/t_tor_root_k.
    DATA lt_stop_link TYPE /bobf/t_frw_key_link.

    " IT_KEY содержит ключи узла ROOT, к которому привязана детерминация.
    " Читаем через IO_READ: в буфере могут быть несохранённые изменения.
    io_read->retrieve(
      EXPORTING iv_node = /scmtms/if_tor_c=>sc_node-root
                it_key  = it_key
      IMPORTING et_data = lt_root ).

    " 1. Фильтр первой строкой: TOR — это ещё и FU, FB, TU.
    "    CHECK: константу категории FO сверьте в /SCMTMS/IF_TOR_CONST
    DELETE lt_root WHERE tor_cat  <> /scmtms/if_tor_const=>sc_tor_category-active
                      OR tor_type <> gc_tor_type.
    IF lt_root IS INITIAL.
      RETURN.
    ENDIF.

    " 2. Стопы всех документов одним вызовом. Данные не нужны, хватит связей.
    io_read->retrieve_by_association(
      EXPORTING iv_node        = /scmtms/if_tor_c=>sc_node-root
                it_key         = CORRESPONDING #( lt_root )
                iv_association = /scmtms/if_tor_c=>sc_association-root-stop   " CHECK
                iv_fill_data   = abap_false
      IMPORTING et_key_link    = lt_stop_link ).

    " 3. Пишем только если значение изменилось: лишний UPDATE запускает
    "    другие детерминации и валидации.
    LOOP AT lt_root REFERENCE INTO DATA(lr_root).
      DATA(lv_count) = REDUCE int4( INIT n = 0
                                    FOR ls_link IN lt_stop_link
                                    WHERE ( source_key = lr_root->key )
                                    NEXT n = n + 1 ).
      IF lv_count = lr_root->zz_stop_count.
        CONTINUE.
      ENDIF.

      lr_root->zz_stop_count = lv_count.
      io_modify->update(
        iv_node           = /scmtms/if_tor_c=>sc_node-root
        iv_key            = lr_root->key
        is_data           = lr_root
        it_changed_fields = VALUE #( ( 'ZZ_STOP_COUNT' ) ) ).
    ENDLOOP.
  ENDMETHOD.

ENDCLASS.
