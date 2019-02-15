# Prostředí a programovací jazyk Selfu (díl třetí; debugger, transporter a problémy)

2019/02/10

Dneska se bude jednat o mezi-díl, kam jsem nacpal věci, jenž se mi moc nevešly nikam jinam. Podíváme se detailněji na debugger a transporter a taky si rozebreme nevýhody Selfu jako jazyka, prostředí, ale i obecně principu používání prototypového programování.

# Z hlediska uživatelského použití transporteru

Nebudu se věnovat tomu, jak přesně transporter funguje, to je možné vyčíst například z paperu [Sifting Out the Gold: Delivering Compact Applications From an Exploratory Object-Oriented Environment](http://bibliography.selflanguage.org/gold.html). Zaměřím se spíš na uživatelskou stránku, tak jak je ukázána ve videu na stránce [https://bluishcoder.co.nz/2015/11/19/exporting-self-objects-to-source-files-via-transporter.html](https://bluishcoder.co.nz/2015/11/19/exporting-self-objects-to-source-files-via-transporter.html).

Obrázkově je tahle podkapitola hrozně dlouhá, proto chci předem říct, že ve skutečnosti se neděje nic moc komplikovaného. Vytvořím anonymní objekt. Přidám ho v transporteru do nového modulu. Pak vytvořím slot v globální hierarchii, uložím do něj tento objekt a taky ho přidám do již vytvořeného modulu. Potom řeknu anotací transporteru, aby slot nenastavoval na defaultní hodnotu, ale „sledoval“ objekt co je v něm uložený. Pak všechno uložím na disk skrz dialog transporteru.

Začnu vytvořením naprosto jednoduchého objektu, obsahujícího jeden slot „a“ o hodnotě „1“.

![](transporter_0-7727dd53-ad6d-49e2-856e-fc86ac5b23f5.png)

![](transporter_1-288e46b8-d6f0-46fb-b5de-e33be86db39a.png)

Na outliner potom kliknu prostředním tlačítkem (kolečkem) a vyberu z menu *„Set module...“*:

![](transporter_2-868281e4-47aa-47a8-8691-78c6451eacdc.png)

Nyní se bude objevovat série dialogů, kde se mě transporter poptá na různé informace. Jako první se ptá na sloty:

![](transporter_3-f205e69c-7558-4391-88bf-ea6f77d9c6e8.png)

Chci všechny.

Dál se ptá na jméno modulu, do kterého objekt uložit.

![](transporter_4-a2ec8578-47f5-48d8-82b3-adcd86f7af13.png)

Chci „other“, což vyvolá dialog s názvem. Já chci svůj modul pojmenovat „test“:

![](transporter_6-2583d8dd-038b-4964-a198-767159ac2dc9.png)

Dialog se mě nyní ptá zda chci modul vytvořit, nebo jsem se splet. Chci ho skutečně vytvořit:

![](transporter_7-982ea53a-2cca-4e29-a58f-45a6b3526aeb.png)

Nechci ho udělat submodulem ostatních modulů, proto nechávám následující pole prázdné:

![](transporter_8-16b1a42a-aaf9-4abc-b07b-59471512a47e.png)

Ještě to znova potvrzuji:

![](transporter_9-fb3e425d-6995-49ea-b5c8-ad1fecffe2c1.png)

Vybírám složku do které by se měl soubor uložit. Nechávám defaultní „applications“:

![](transporter_10-81fd3acf-d90d-4965-95f8-410932e9f1ab.png)

Můj objekt je nyní oficiálně součástí modulu, akorát se prostě jen tak vznáší ve vzduchu, což znamená, že by po načtení nešel moc dobře referencovat. Já ho chci uložit na cestu `globals test`. Otevřu si tedy outliner pro `globals` kliknutím na plochu kolečkem:

![](transporter_11-4472d7d8-a4c7-435f-b66c-ee94490c62c0.png)

a otevřu si podsekci „applications“:

![](transporter_12-a1a4227a-417a-45b7-aeeb-6f6e709c2487.png)

Vidím, že už v ní jsou čtyři aplikace. Kliknutím na nápis „applications“ prostředním se objeví kontextové menu, kde vyberu „Add Slot“:

![](transporter_13-be658c08-d5cf-4755-b841-46cf3a81a013.png)

Z dialogu pro přidání slotu smažu defaultní text s nápovědou:

![](transporter_14-753cea45-a3cf-4428-a100-3b43531393ff.png)

a nastavím slot na `nil`.

![](transporter_16-65ea4d39-9b28-4083-8e04-ffc8c1a903bc.png)

Uložím kliknutím na zelený obdélník, či stisknutím CTRL+enter.

![](transporter_17-0254c460-d4bb-4e19-9ba4-897b2000450f.png)

Nyní místo `nil`u graficky přenesu referenci na můj anonymní objekt na ploše. Stejně tak bych ale mohl přijít do mého anonymního objektu, otevřít si v něm shell a zadat cosi jako `globals test: self`.

![](transporter_18-db54e536-91a2-45cd-8729-504d37aba7c0.png)

![](transporter_19-a7dda282-31b0-495d-b978-afce9218e1a4.png)

![](transporter_20-475637fe-b23c-45e0-a1f1-b237e10bcea3.png)

Slot `globals test` nyní ukazuje na můj objekt, neboli můj objekt nyní existuje na této cestě.

Nyní zbývá ještě nastavit modul pro tento slot kliknutím prostředním tlačítkem a vybráním „Set module“:

![](transporter_21-c94a7424-3f34-4f6c-8597-e8308f8d3ec5.png)

Zobrazí se podstatně větší menu, kde doscrolluju až dolu a vyberu other:

![](transporter_22-c2fe4608-e4e6-4ab8-87af-341e2b44632f.png)

Tam znova zadám „test“:

![](transporter_23-cdec761a-7657-4a96-8dbb-8c73df2d7860.png)

Abych teď nemusel jak blázen scrollovat zase nahoru, dvakrát kliknu na prázdnou plochu a vyberu že chci jít „home“:

![](transporter_24-18c87ab9-1390-4abd-9d14-7d94345682a5.png)

Což mě vrátí tam kde jsem byl. Nyní ještě potřebuji upravit anotaci slotu `globals test`, kliknu na něj tedy opět kolečkem a vyberu „Show Annotation“:

![](transporter_29-b81dc6e6-62a9-49fe-8491-eb8267203879.png)

V nastavení modulu vyberu že chci „Follow“, nikoliv nastavovat slot na `nil`.

![](transporter_30-684486ff-bfc1-48b3-895e-2f96240e8121.png)

![](transporter_31-4b662112-9cfe-452f-8999-de22c4262880.png)

Nyní kliknu do prázdného místa na ploše prostředním a vyberu z menu „Changed Modules“:

![](transporter_25-3e4cbbae-3ce7-416e-811b-a2fc3344f040.png)

Zobrazí se mi dialog ukazující změněné moduly:

![](transporter_26-ca533ad5-0ddf-487c-ab70-49eb3589eae5.png)

Ty můžu zapsat klikáním na tlačítka. Kliknu na tlačítko s nápisem „W“ vedle:

![](transporter_27-16442526-e10b-4909-8528-f66f9fadbf01.png)

Tak a to je vše. Zdá se to jako hodně kroků, ale ve skutečnosti je to celé docela logické. Nyní se můžu podívat, že o úroveň výš (neptejte se mě proč) vznikl ve složce „objects/applications/“ soubor „test.self“:

    ''
     '
    Copyright 1992-2016 AUTHORS.
    See the legal/LICENSE file for license information and legal/AUTHORS for authors.
    '
    [ 
    "prefileIn" self] value
    
    
     '-- Module body'
    
     bootstrap addSlotsTo: bootstrap stub -> 'globals' -> 'modules' -> () From: ( | {
             'ModuleInfo: Module: test InitialContents: FollowSlot'
            
             test = bootstrap define: bootstrap stub -> 'globals' -> 'modules' -> 'test' -> () ToBe: bootstrap addSlotsTo: (
                 bootstrap remove: 'directory' From:
                 bootstrap remove: 'fileInTimeString' From:
                 bootstrap remove: 'myComment' From:
                 bootstrap remove: 'postFileIn' From:
                 bootstrap remove: 'revision' From:
                 bootstrap remove: 'subpartNames' From:
                 globals modules init copy ) From: bootstrap setObjectAnnotationOf: bootstrap stub -> 'globals' -> 'modules' -> 'test' -> () From: ( |
                 {} = 'ModuleInfo: Creator: globals modules test.
    
    CopyDowns:
    globals modules init. copy 
    SlotsToOmit: directory fileInTimeString myComment postFileIn revision subpartNames.
    
    \x7fIsComplete: '.
                | ) .
            } | ) 
    
     bootstrap addSlotsTo: bootstrap stub -> 'globals' -> 'modules' -> 'test' -> () From: ( | {
             'ModuleInfo: Module: test InitialContents: FollowSlot\x7fVisibility: public'
            
             directory <- 'applications'.
            } | ) 
    
     bootstrap addSlotsTo: bootstrap stub -> 'globals' -> 'modules' -> 'test' -> () From: ( | {
             'ModuleInfo: Module: test InitialContents: InitializeToExpression: (_CurrentTimeString)\x7fVisibility: public'
            
             fileInTimeString <- _CurrentTimeString.
            } | ) 
    
     bootstrap addSlotsTo: bootstrap stub -> 'globals' -> 'modules' -> 'test' -> () From: ( | {
             'ModuleInfo: Module: test InitialContents: FollowSlot'
            
             myComment <- ''.
            } | ) 
    
     bootstrap addSlotsTo: bootstrap stub -> 'globals' -> 'modules' -> 'test' -> () From: ( | {
             'ModuleInfo: Module: test InitialContents: FollowSlot'
            
             postFileIn = ( |
                | resend.postFileIn).
            } | ) 
    
     bootstrap addSlotsTo: bootstrap stub -> 'globals' -> 'modules' -> 'test' -> () From: ( | {
             'ModuleInfo: Module: test InitialContents: InitializeToExpression: (\'30.21.0\')\x7fVisibility: public'
            
             revision <- '30.21.0'.
            } | ) 
    
     bootstrap addSlotsTo: bootstrap stub -> 'globals' -> 'modules' -> 'test' -> () From: ( | {
             'ModuleInfo: Module: test InitialContents: FollowSlot\x7fVisibility: private'
            
             subpartNames <- ''.
            } | ) 
    
     bootstrap addSlotsTo: bootstrap stub -> 'globals' -> () From: ( | {
             'Category: applications\x7fModuleInfo: Module: test InitialContents: FollowSlot'
            
             test <- bootstrap setObjectAnnotationOf: bootstrap stub -> 'globals' -> 'test' -> () From: ( |
                 {} = 'ModuleInfo: Creator: globals test.
    '.
                | ) .
            } | ) 
    
     bootstrap addSlotsTo: bootstrap stub -> 'globals' -> 'test' -> () From: ( | {
             'ModuleInfo: Module: test InitialContents: FollowSlot'
            
             a = 1.
            } | ) 
    
    
    
     '-- Side effects'
    
     globals modules test postFileIn

V něm jsou nastaveny všechna možná metadata. Tento soubor můžu verzovat gitem a také načíst do nové image:

![](transporter_33-056a05ed-17ea-4c4f-b140-542f066ae34e.png)

Což mi dá do ruky metadata o modulu a vedle v outlineru pro `globals` si můžete všimnout že se objevil nový slot „test“:

![](transporter_34-be139fd7-d1fd-49d7-a5ae-93763a728e1d.png)

Ve kterém je skutečně můj objekt:

![](transporter_35-702d6808-3bd3-4b58-a3bd-ec9dd1695426.png)

# Z hlediska debuggeru

Self nabízí debugger smalltalkovského typu, ze kterého je možné interaktivně měnit kód. Krátká ukázka myslím řekne víc než tisíc slov.

V Shellu vytvořím jednoduchý objekt, který má slot „a“, kde je uložen kód, který by měl na standardní výstup vypsat hodnotu čísla „1“. Záměrně se ale upíši a místo zprávy „`printLine`“ pošlu pouze zprávu „`printLin`“, tedy bez „`e`“ na konci:

![](debugger_0-15027ba0-85d2-45ba-a97f-2372bbb51bbb.png)

To mi *„do ruky“* vloží objekt, který jsem popsal.

![](debugger_1-7e8e872f-e14c-42c8-a99c-6e8e72859223.png)

Můžu si zkontrolovat, že je to skutečně on tím že ho položím na plochu a rozbalím sloty:

![](debugger_2-284f160d-55cb-4143-a4a4-dd788f091db5.png)

V objektu otevřu *podshell* kliknutím na E vpravo v rohu a pošlu mu zprávu „a“:

![](debugger_3-cb9275c3-16e6-438e-9d64-43c83a65eae2.png)

Nyní kliknu na *Get it*, což by mělo kód provést (tedy vypsat do konzole jedničku) a zároveň mi do kurzoru umístit výsledek volání (také jednička). V kódu mám ale popsanou chybu, takže místo toho dostanu do ruky debugger:

![](debugger_4-821aa58c-9a8d-4b18-8146-48498672ba19.png)

Debugger vypadá trochu podobně jako outliner. Krabička, která se dá rozklikávat. Zde je celá rozkliknutá:

![](debugger_5-3e4dd51b-566e-40c4-8a99-feb9f0536e45.png)

Můžeme vidět celý stack trace, ale nejenom to, dá se s ním krásně interagovat. Například vlevo nahoře vidíme jedničku, což je receiver zprávy (selektoru). Na jedničku lze kliknout a dostaneme přímo objekt:

![](debugger_6-4436f06e-da30-444a-8416-7acf4c780091.png)

![](debugger_7-804c954a-13f8-4063-8586-a713b419a210.png)

V případě jedničky to sice úplně nedává smysl, ale u jiných objektů může být velmi užitečné si je živě prozkoumat.

Z editoru lze také chybu hned opravit:

![](debugger_8-1cfdf231-8c69-4b6f-9d7f-725c26ce62a6.png)

Po kliknutí na zelený čtvereček se upraví přímo kód, všimněte si outlineru vedle:

![](debugger_9-36cb0358-afb5-4c5a-bd17-44269e446b7c.png)

Nyní kliknu na continue a celý interpret bude pokračovat tam, kde by pokračoval normálně, kdyby k žádné chybě nedošlo, tedy do konzole se vypíše jednička a ta se mi taky octne v ruce:

![](debugger_11-11917759-c815-46e7-9bba-98b80641d2e7.png)

Debugger nyní vypíše, že je mrtvý a minimalizuje se. Když nyní znova kliknu na *Get it* tlačítko, vše již napodruhé proběhne správně;

![](debugger_13-056babea-1e93-476c-a226-3aa4a61f5916.png)

# Z hlediska problémů

Z praktického hlediska je Self docela smutná kupka. Nejprve bych rád řekl, že je do velké míry použitelný, ale zdaleka ne tolik, aby to bylo přístupné pro začínající uživatele. Pokud něco budete řešit, zapomeňte na to, že vygooglíte řešení. S vysokou pravděpodobností jste nejspíš první, kdo má daný problém. A pokud ne, tak je stejně slušná šance, že problém je nevyřešen.

## 32 bit

Self je 32 bitový program. Portace na 64 bitů je sice možná, ale netriviální a nikdo se do toho nehrne. Očekávám, že v příštích deseti letech se na tom asi nic nezmění.

Na jednu stranu je to docela nemilé, protože vás to omezuje na maximálně čtyřgigabajtové image, ale tenhle problém se dá vyřešit například použitím víc instancí a hlavně narazíte na problémy se vším možným daleko dřív. Například samotné ukládání image je docela pomalé už u velikostí kolem desítek megabajtů a gigabajtové velikosti by trvaly pravděpodobně celé minuty.

## Problémy prototypů

Prototypy jsou jednoduché na pochopení a spolu s delegaci (koukám se na tebe, javascripte!) nabízejí silný a efektivní mechanismus organizace kódu.

Mají ovšem jednu nevýhodu; jednou zapomenete na clone a přepíšete půlku systému.

Například s prototypovým `dictionary` se pracuje prostě tak, že si ho naklonujete a zapisujete do něj hodnoty. Pokud ovšem zapomenete provést klonování a rovnou píšete do dictionary, píšete zároveň do všech nových dictionary co budou vytvořeny kopírováním. To většinou vede k velmi rychlému pádu systému.

Self bohužel nenabízí žádnou možnost, jak se tomuhle bránit. Osobně bych se tomu ve svém jazyce rád vyvaroval *zamykáním* systémových objektů tak, aby bylo vynuceno klonování předtím, než je možné do nich zapsat. Nebo možná nějakým automatickým klonováním.

## Bezejmennost prototypových objektů

Selfovské je na tom se svými literály (zkrácený nativní zápis definice objektu) podobně, jako jazyky podporující pouze lambda funkce. Anonymní objekty jsou super, ale přeci jen člověk se snáze orientuje pokud může věci pojmenovat.

V Selfu je toto řešeno anotacemi, kde je možné nastavit jméno objektu, které se pak zobrazuje v outlinerech, nebo prostě umístěním objektu do patřičné hierarchie. Pokud umístíme objekt do cesty `globals dictionary`, tak je asi jasné, že se jedná o slovník.

Stojí za zamyšlení si to srovnat s *na třídách založenými jazyky*, které zpravidla trpí přesně opačným problémem, kde se snaží pojmenovat úplně všechno. Třída má svoje jasně dané jméno a instance má jméno proměnné kde existuje.

Co je pro lidi lepší a přirozenější? Aby měl objekt jasně dané jméno, nebo aby bylo jméno dané proměnou (či cestou) ve které je uložený?

## No undo

Edit morphy nepodporují undo. Pešek. A všechny ostatní klávesové zkratky jsou nějaký subset části emacsu.

## Ctrl+c / Ctrl+v

Bohužel nefunguje, protože používá nějaké prehistorické X bindingy. Řešení je nainstalovat si program [autocutsel](https://www.nongnu.org/autocutsel/) a pustit ho na pozadí.

## Chybějící dokumentace

Dokumentace prostě kromě toho co jsem už odkazoval není. Většinou se dá zeptat v konferenci, ale to není zrovna ideální.

## Sloty jsou unordered

To je trochu smutné z hlediska používání objektů samotných k uchovávání informací, neboť vás to nutí používat ordered kolekce.

## Self nemá podporu kaskádování

Pokud nevíte co to je, tak vám to asi vadit nebude, přicházíte-li ale ze Smalltalku, tak to bude bolest.

## Unicode vstup / výstup se nekoná

Self používá jako kódování ISO 8859-1, takže nebere žádné znaky mimo toto (doslova se nedají napsat) a nic mimo toho ani neumí zobrazit.

Pokud by se s tím někomu chtělo zabývat, tak zde:

- [https://github.com/russellallen/self/issues/113](https://github.com/russellallen/self/issues/113)

## Outlinery sajou

Outlinery jsou zajímavý koncept, který ale začne být otravný docela rychle. Proč je možné vidět například zde:

- [http://kitakitsune.org/ltas/long_outliner_is_long/traits_xlib_display/](http://kitakitsune.org/ltas/long_outliner_is_long/traits_xlib_display/)

či ve své plné kráse zde:

- [http://kitakitsune.org/ltas/long_outliner_is_long/traits_xlib_display_expanded/](http://kitakitsune.org/ltas/long_outliner_is_long/traits_xlib_display_expanded/)

Taky když zkoumáte nějakou komplexnější věc, tak končíte s desítkami outlinerů.

Osobně bych to doplnil browserem modulů ve stylu Smalltalku:

![](smalltalk_code_browser-b693420e-2760-41f5-be79-b9fdc4c49e4f.png)

## Self a obrázky

Self neumí zobrazovat obrázky v žádném z normálních formátů. Jediné co umí je nějaký [Sunovský rastrový formát](https://en.wikipedia.org/wiki/Sun_Raster):

- [https://bluishcoder.co.nz/2009/07/27/displaying-images-with-self.html](https://bluishcoder.co.nz/2009/07/27/displaying-images-with-self.html)

# Pokračování

V posledním díle se podíváme na komunitu kolem Selfu, historii, budoucnost a dojde i na nějaké to filosofování.