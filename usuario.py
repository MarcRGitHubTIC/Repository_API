def alum_schema(alumno) -> dict:
    return {"userid": alumno[0],
            "nombre": alumno[1],
            "mail": alumno[2],
            "passwd": alumno[3],
            "rol": alumno[4],
            "cardid": alumno[5]
            }

def alumnos_schema(alumnos) -> dict:
    return [alum_schema(alumno) for alumno in alumnos]

