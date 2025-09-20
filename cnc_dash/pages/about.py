import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/about", name="About & notes")

layout = dbc.Container(
    [
        # Botón para volver
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("← Volver al inicio", href="/", color="secondary", outline=True),
                    width="auto",
                )
            ],
            className="mt-3 mb-2",
        ),

        # Tarjeta de contenido (tema claro)
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("About & notes", className="mb-3"),

                                html.P(
                                    "Este tablero busca analizar la adopción digital en Colombia a partir de información sociodemográfica y de conectividad. El caso aborda la identificación de brechas en el acceso a servicios, la calidad de la conexión y la disponibilidad de dispositivos, con el fin de diferenciar perfiles de usuarios y territorios."

                                    "La finalidad es ofrecer una herramienta visual que permita a tomadores de decisiones detectar poblaciones rezagadas, priorizar intervenciones por región y diseñar estrategias focalizadas. El tablero integra mapas, indicadores clave y resúmenes por clúster para apoyar la formulación de políticas y programas que impulsen la adopción digital inclusiva en el país.",
                                    className="mb-3",
                                ),

                                html.H5("Perfiles de clúster"),
                                html.P("Entre paréntesis, el porcentaje del total de observaciones.", className="mb-2"),

                                html.Ul(
                                    [
                                        html.Li(
                                            [
                                                html.Strong("C6 (23.5%) — Conectados con interrupciones en zonas bajo promedio. "),
                                                "Servicios sí (~0.99), conexión hogar sí (~0.99), interrupciones sí (1.0), dens_int −0.84. ",
                                                html.Em("Lectura: grandes bolsas de usuarios conectados pero en territorios menos favorecidos; la confiabilidad es el dolor principal."),
                                            ]
                                        ),
                                        html.Li(
                                            [
                                                html.Strong("C0 (12.5%) — Conectados, sin interrupciones, en territorios bajo promedio. "),
                                                "Conexión hogar 1.0, interrupciones 0.0, dens_int −0.85. ",
                                                html.Em("Lectura: buen servicio pese al contexto; mantener y escalar buenas prácticas."),
                                            ]
                                        ),
                                        html.Li(
                                            [
                                                html.Strong("C2 (14.2%) y C1 (5.9%) — Conectados con interrupciones; contextos distintos. "),
                                                "Conexión hogar ≈1.0, interrupciones 1.0; dens_int ≈0.07 (C2) y 1.01 (C1). ",
                                                "Top departamentos sugieren sesgos regionales (p.ej., C1: Norte de Santander 33%; C2: Atlántico 45%). ",
                                                html.Em("Lectura: mismo dolor (interrupciones), contextos opuestos → acciones regionales diferenciadas."),
                                            ]
                                        ),
                                        html.Li(
                                            [
                                                html.Strong("C8 (4.0%) y C10 (2.5%) — Alta densidad territorial; trayectorias opuestas. "),
                                                "C8: conexión hogar 1.0, interrupciones 0.32, dens_int 2.43 → adopción alta con retos de confiabilidad. ",
                                                "C10: servicios sí 0.86, conexión hogar 0.0, muchos sin dispositivos (0.57), dens_int 2.64 → zonas favorecidas pero hogar desconectado y sin equipos. ",
                                                html.Em("Lectura: priorizar continuidad (C8) y cerrar brecha de acceso/dispositivos (C10)."),
                                            ]
                                        ),
                                        html.Li(
                                            [
                                                html.Strong("C3 (5.5%) y C4 (7.5%) — Barrera de equipos / hogar desconectado. "),
                                                "C3: servicios sí 0.94, dispositivos_no 0.57, conexión 0.0, dens_int 1.21. ",
                                                "C4: servicios sí 1.0, dispositivos_no 1.0, conexión 0.0, dens_int −0.39. ",
                                                html.Em("Lectura: cuello de botella en equipamiento y conexión fija; C3 en zonas sobre promedio (alto potencial), C4 en zonas bajo promedio (requerirá infraestructura + dispositivos)."),
                                            ]
                                        ),
                                        html.Li(
                                            [
                                                html.Strong("C9 (4.5%) — Doble brecha (servicios y dispositivos). "),
                                                "Servicios_No 1.0, conexión hogar ~0.10, dispositivos_no 0.64, dens_int −0.15. ",
                                                html.Em("Lectura: casi offline; requiere paquetes integrales (cobertura, asequibilidad, dotación, formación)."),
                                            ]
                                        ),
                                        html.Li(
                                            [
                                                html.Strong("C5 (5.5%) y C7 (5.3%) — Casos mixtos. "),
                                                "C5: conectados, sin interrupciones, dens_int 1.12 → maduro (mantener calidad). ",
                                                "C7: servicios sí, sin conexión fija (0.0), pocas interrupciones, dens_int −0.40 → uso móvil-céntrico sin banda ancha fija. ",
                                                html.Em("Lectura: acciones de migración a fijo/planes hogar (C7)."),
                                            ]
                                        ),
                                    ],
                                    className="mb-4",
                                ),

                                html.H5("¿Cómo responde esto a la pregunta de negocio?"),
                                html.Ul(
                                    [
                                        html.Li(
                                            [
                                                html.Strong("Identificación de poblaciones rezagadas: "),
                                                "Dispositivos/hogar desconectado (C3, C4, C10, C9); ",
                                                "calidad de servicio/interrupciones (C1, C2, C6, C8); ",
                                                "uso móvil sin banda ancha fija (C7).",
                                            ]
                                        ),
                                        html.Li(
                                            [
                                                html.Strong("Focalización territorial: "),
                                                "apoyarse en la distribución por departamento/municipio de cada clúster (y su entropía) "
                                                "para priorizar regiones piloto y asignar responsables.",
                                            ]
                                        ),
                                        html.Li(
                                            [
                                                html.Strong("Diseño de intervención: "),
                                                "Dispositivos + asequibilidad + alfabetización (C3/C4/C10/C9); ",
                                                "mejoras de continuidad/infraestructura (C1/C2/C6/C8); ",
                                                "migración a fijo/planes hogar (C7).",
                                            ]
                                        ),
                                    ],
                                    className="mb-4",
                                ),

                                html.H6("Notas metodológicas"),
                                html.Ul(
                                    [
                                        html.Li("Los porcentajes corresponden a la participación de cada clúster sobre el total de observaciones."),
                                        html.Li("Variables como dens_int están estandarizadas (0 ≈ promedio)."),
                                        html.Li("Estos perfiles orientan decisiones; los umbrales/curvas de intervención pueden ajustarse con evidencia adicional."),
                                    ]
                                ),
                            ]
                        ),
                        className="card-light",  # fuerza fondo blanco + texto oscuro
                    ),
                    md=12,
                )
            ],
            className="about-light",
        ),
    ],
    fluid=True,
)