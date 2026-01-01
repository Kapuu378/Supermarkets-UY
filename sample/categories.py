devoto = {
    "ALMACEN":{
        "CANASTA FAMILIAR":['/412/413/435/', '/412/413/436/','/412/413/437/','/412/413/438/', '/412/413/439/', '/412/413/440/', '/412/413/443/', '/412/413/445/', '/412/413/446/', '/412/413/448/', '/412/413/449/', '/412/413/452/', '/412/413/455/', '/412/413/460/', '/412/413/502/', '/412/413/547/', '/412/413/557/'],
        "DESAYUNO MERIENDA Y POSTRES":['/412/414/417/', '/412/414/418/', '/412/414/419/', '/412/414/420/', '/412/414/421/', '/412/414/422/', '/412/414/423/', '/412/414/424/', '/412/414/425/', '/412/414/426/', '/412/414/427/', '/412/414/428/', '/412/414/429/', '/412/414/430/', '/412/414/431/', '/412/414/432/', '/412/414/433/', '/412/414/434/']
    },
    "PERFUMERIA Y LIMPIEZA":{
        "PERFUMERIA":['/476/477/479/', '/476/477/481/', '/476/477/485/', '/476/477/486/', '/476/477/487/', '/476/477/488/', '/476/477/490/', '/476/477/491/', '/476/477/492/', '/476/477/494/', '/476/477/495/', '/476/477/496/', '/476/477/498/', '/476/477/499/', '/476/477/501/'],
        "LIMPIEZA":['/476/478/480/', '/476/478/482/', '/476/478/483/', '/476/478/484/', '/476/478/489/', '/476/478/493/', '/476/478/497/', '/476/478/500/']
    },
    "FRESCOS":{
        "CONGELADOS":['/539/415/'],
        "LACTEOS":['/539/416/'],
        "CARNICERIA":['/539/503/'],
        "FIAMBRES":['/539/504/'],
        "QUESOS":['/539/505/'],
        "ROSTISERIA":['/539/506/'],
        "PANADERIA":['/539/507/'],
        "CONFITERIA":['/539/508/'],
        "PESCADERIA":['/539/509/'],
        "FRUTAS Y VERDURAS":['/539/510/'],
        "PASTAS":['/539/536/']
    },
    "BEBIDAS":{
        "VINOS FINOS":['/350/351/'],
        "AGUA":['/350/387/'],
        "BEBIDAS BLANCAS":['/350/388/'],
        "DESTILADAS":['/350/389/'],
        "CERVEZAS":['/350/390/'],
        "APERITIVOS":['/350/391/'],
        "ENERGETICAS":['/350/392/'],
        "VINOS":['/350/395/'],
        "REFRESCOS":['/350/471/'],
        "JUGOS EN POLVO":['/350/473/'],
        "JUGOS":['/350/474/']
    }
}

def get_devoto_categories()->list[str]:
    result = []
    
    for sub_category in devoto.values():
        for list in sub_category.values():
            result.extend(list)

    return result

eldorado = {
    "COMESTIBLES":{
        "ALMACEN":['/2/16/'],
        "CONGELADOS":['/2/18/'],
        "ELABORACION PROPIA":['/2/19/'],
        "GOLOSINAS":['/2/21/'],
        "PANADERIA":['/2/23/']
    },
    "CUIDADO PERSONAL":{
        "BEBES":['/3/27/'],
        "CUIDADO CAPILAR":['/3/29/'],
        "CUIDADO CORPORAL":['/3/30/'],
        "HIGIENE BUSCAL":['/3/31/']
    },
    "LIMPIEZA":{
        "CUIDADO DE LA ROPA":['/8/59/'],
        "INSECTICIDAS":['/8/62/'],
        "LIMPIEZA HOGAR":['/8/63/'],
        "LIMPIEZA MARCAS PROPIAS":['/8/64/']
    },
    "FRESCOS":{
        "CARNICERIA":['/20/17/'],
        "LACTEOS":['/20/22/'],
        "FRUTAS Y VERDURAS":['/20/24/'],
        "ENVASADO AL VACIO":['/20/173/'],
        "FIAMBRERIA":['/20/174/'],
        "POSTRES":['/20/175/'],
        "PASTAS FRESCAS":['/20/235/']
    },
    "BEBIDAS":{
        "CON ALCOHOL":['/1/14/'],
        "SIN ALCOHOL":['/1/15/']
    }
}

def get_eldorado_categories()->list[str]:
    result = []
    
    for sub_category in eldorado.values():
        for list in sub_category.values():
            result.extend(list)

    return result