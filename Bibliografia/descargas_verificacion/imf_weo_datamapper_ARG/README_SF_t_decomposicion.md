# Fuentes para la descomposición ilustrativa del Ajuste Stock-Flujo (SF_t), Hallazgo H3

Descargado el 4 de agosto de 2026 desde la API pública del IMF DataMapper
(`https://www.imf.org/external/datamapper/api/v1/<indicador>/ARG`), sin necesidad
de autenticación. Los 4 archivos JSON de esta carpeta son la respuesta cruda de la
API, sin modificar.

| Archivo | Indicador IMF | Descripción | URL exacta |
|---|---|---|---|
| `GGXCNL_NGDP_overall_balance.json` | `GGXCNL_NGDP` | General government net lending/borrowing (resultado global), % PIB | https://www.imf.org/external/datamapper/api/v1/GGXCNL_NGDP/ARG |
| `pb_primary_balance.json` | `pb` | Government primary balance (resultado primario), % PIB. Nota: esta serie proviene de la base "Public Finances in Modern History" del FMI (Mauro et al.), que cubre 1800--2024 | https://www.imf.org/external/datamapper/api/v1/pb/ARG |
| `GGXWDG_NGDP_gross_debt.json` | `GGXWDG_NGDP` | General government gross debt, % PIB | https://www.imf.org/external/datamapper/api/v1/GGXWDG_NGDP/ARG |
| `PCPIPCH_inflation.json` | `PCPIPCH` | Inflación, precios al consumidor, variación % promedio anual | https://www.imf.org/external/datamapper/api/v1/PCPIPCH/ARG |

## Uso y limitaciones — leer antes de citar

Estas 4 series se usaron **exclusivamente** para aproximar una tasa de interés real
efectiva ($r_t$) sobre la deuda pública argentina en 2005, 2018 y 2020, con el único
fin de ilustrar la descomposición del Ajuste Stock-Flujo ($SF_t$) discutida en la
Sección 7.2 de la tesis (Hallazgo H3 de `plan_implementacion_revision_pares.md`).
**No reemplazan, ni pretenden reemplazar, ninguna serie propia del dataset de la
tesis** (`data/dataset_consolidado_real.csv`).

Limitaciones explícitas de esta aproximación (documentadas también en el cuerpo de
la tesis):

1. **Perímetro distinto**: estas series del FMI son de "general government"
   (gobierno general, consolidado nación + provincias en la metodología del FMI),
   mientras que $d_t$, $d_{t-1}$ y $pb_t$ de la tesis son del Sector Público No
   Financiero consolidado con los pasivos remunerados del BCRA. No son el mismo
   perímetro institucional.
2. **Tasa nominal implícita, no observada directamente**: $i_t$ se calculó como
   (resultado primario FMI $-$ resultado global FMI) $/$ deuda FMI del año
   anterior, es decir, un intereses/deuda implícito, no una tasa de mercado
   observada ni una tasa efectiva de la cartera de pasivos argentina.
3. **Conversión a tasa real vía Fisher con inflación del FMI**: la inflación
   argentina es una magnitud estadísticamente disputada (la serie oficial INDEC
   2007-2015 fue objeto de una advertencia formal del FMI por subestimación). La
   serie `PCPIPCH` del FMI es la estimación propia del staff del FMI, no
   necesariamente idéntica al IPC oficial de INDEC vigente en cada período.
4. Por los tres puntos anteriores, el $SF_t$ resultante es una **aproximación de
   orden de magnitud, no una serie propia de la tesis con el mismo estatus
   evidencial que las estimaciones econométricas del Capítulo 6**. Se presenta en
   el cuerpo de la tesis con esa calificación explícita.
