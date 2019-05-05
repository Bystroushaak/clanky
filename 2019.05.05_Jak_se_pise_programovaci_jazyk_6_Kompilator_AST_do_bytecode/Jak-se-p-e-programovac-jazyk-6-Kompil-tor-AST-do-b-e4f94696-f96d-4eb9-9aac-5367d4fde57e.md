# Jak se píše programovací jazyk 6: Kompilátor AST do bytecode

V minulém díle jsem rozepsal jak vypadají moje bajtkódy. Jak se k nim ale dostat? Přes moje původní obavy se ukázalo, že neoptimalizující kompilátor je v případě, že existuje abstraktní syntaktický strom krásně jednoduchý.

Ke každému prvku AST stromu jsem přidal metodu `.compile(code_context)`, která do `code_context` objektu zkompiluje sebe sama, tedy vloží do něj patřičné literály a do bajtkódu vloží instrukce pro jejich použití.

Například pro objekt Self to vypadá takto:

    def compile(self, context):
        context.add_bytecode(BYTECODE_PUSH_SELF)
    
        return context

Pro objekt představující čísla už je to trochu složitější, neboť je třeba prvně číslo vložit do seznamu literálů:

    def compile(self, context):
        index = context.add_literal_int(self.value)
    
        context.add_bytecode(BYTECODE_PUSH_LITERAL)
        context.add_bytecode(LITERAL_TYPE_INT)
        context.add_bytecode(index)
    
        return context

V bajtkódu je vložená instrukce `PUSH_LITERAL`, poté typ literálu a jeho index.

U binární zprávy je krásně vidět, jak se prvně zkompiluje čemu se má zpráva poslat a poté teprve samotná zpráva:

    def compile(self, context):
        context.add_literal_str_push_bytecode(self.name)
    
        self.parameter.compile(context)
    
        context.add_bytecode(BYTECODE_SEND)
        context.add_bytecode(SEND_TYPE_BINARY)
        context.add_bytecode(1)
    
        return context

Prvně se resolvne název, poté se zkompiluje obsah parametru a poté se tento obsah pošle objektu na názvu. Poslední řádek `context.add_bytecode(1)` určuje počet parametrů, což je u binárních zpráv vždy jeden.

Krásně se to kombinuje s objektem `Send`, který specifikuje fakt že se má něco něčemu poslat:

    def compile(self, context):
        self.obj.compile(context)
        self.msg.compile(context)
    
        return context

Prvně zkompiluj objekt kterému bude něco posílat, což muže být třeba `Self`, poté samotnou zprávu, což může být třeba výše uvedená `BinaryMessage`.

Asi nejzajímavějším a nejsložitějším na zkompilování se ukázal `Object`:

    def _add_slot_to_bytecode(self, context, name, value):
        boxed_name = String(name)
        boxed_name.compile(context)
    
        value.compile(context)
    
        context.add_bytecode(BYTECODE_ADD_SLOT)
    
    def compile(self, context):
        obj = ObjectRepresentation()
        obj.meta_set_ast(self)
        obj.meta_set_parameters(self.params)
    
        index = context.add_literal_obj(obj)
        context.add_bytecode(BYTECODE_PUSH_LITERAL)
        context.add_bytecode(LITERAL_TYPE_OBJ)
        context.add_bytecode(index)
    
        for name, value in self.slots.iteritems():
            self._add_slot_to_bytecode(context, name, value)
            context.add_bytecode(SLOT_NORMAL)
    
        for name, value in self.parents.iteritems():
            self._add_slot_to_bytecode(context, name, value)
            context.add_bytecode(SLOT_PARENT)
    
        if self.code:
            new_context = CodeContext()
            obj.meta_set_code_context(new_context)
            for item in self.code:
                item.compile(new_context)
    
            obj.map.code_context = new_context
    
        return context

Složitost je do velké míry dána tím, že jsem se rozhodl, že objektové literály budu vkládat mezi literály jako poměrně jednoduché objekty, které nemají nic moc kromě parametrů předvyplněno. Vyplnění probíhá ve chvíli, kdy je objekt vytvořen.

Výše je možné vidět, že je nejdřív vytvořen prázdný objekt, do kterého je uložena jen AST reprezentace pro pozdější referenci a seznam parametrů, které přijímá. Celý zbytek je pak dodán až dynamicky za běhu - všechny *sloty*, všechny *parent sloty* a samozřejmě když obsahuje kód, tak je vše rekurzivně provedeno i pro kód.

## Disassembler

Když už jsem měl hotový triviální kompilátor, rozhodl jsem se také napsat si k němu jednoduchý disassembler, tedy něco co mi poněkud lečeji zobrazí zkompilovaný kód. V podstatě to funguje inverzně ke kompilátoru; postupně bere instrukce a jejich parametry a překládá je na mnemotechnické zkratky instrukcí:

Napsal jsem to celé maximálně triviálně:

    def _compute_index(bytecodes_len, bytecodes):
        return str(bytecodes_len - len(bytecodes))
    
    
    def disassemble(bytecodes_bytearray):
        disassembled = []
    
        bytecodes = [ord(c) for c in bytecodes_bytearray]
        bytecodes_len = len(bytecodes)
        while bytecodes:
            index = _compute_index(bytecodes_len, bytecodes)
            bytecode = bytecodes.pop(0)
    
            if bytecode == BYTECODE_SEND:
                send_type = bytecodes.pop(0)
    
                send_type_str = {
                    SEND_TYPE_UNARY: "UNARY",
                    SEND_TYPE_BINARY: "BINARY",
                    SEND_TYPE_KEYWORD: "KEYWORD",
                    SEND_TYPE_UNARY_RESEND: "UNARY_RESEND",
                    SEND_TYPE_KEYWORD_RESEND: "KEYWORD_RESEND",
                }[send_type]
    
                number_of_params = bytecodes.pop(0)
    
                disassembled.append([
                    index,
                    "SEND",
                    "type:" + send_type_str,
                    "params:" + str(number_of_params)
                ])
                continue
    
            elif bytecode == BYTECODE_PUSH_SELF:
                disassembled.append([
                    index,
                    "PUSH_SELF"
                ])
                continue
    
            elif bytecode == BYTECODE_PUSH_LITERAL:
                literal_type = bytecodes.pop(0)
                literal_index = bytecodes.pop(0)
    
                literal_type_str = {
                    LITERAL_TYPE_NIL: "NIL",
                    LITERAL_TYPE_INT: "INT",
                    LITERAL_TYPE_STR: "STR",
                    LITERAL_TYPE_OBJ: "OBJ",
                    LITERAL_TYPE_FLOAT: "FLOAT",
                    LITERAL_TYPE_BLOCK: "BLOCK",
                    LITERAL_TYPE_ASSIGNMENT: "ASSIGNMENT",
                }[literal_type]
    
                disassembled.append([
                    index,
                    "PUSH_LITERAL",
                    "type:" + literal_type_str,
                    "index:" + str(literal_index)
                ])
                continue
    
            elif bytecode == BYTECODE_RETURN_TOP:
                disassembled.append([
                    index,
                    "RETURN_TOP"
                ])
                continue
    
            elif bytecode == BYTECODE_RETURN_IMPLICIT:
                disassembled.append([
                    index,
                    "RETURN_IMPLICIT"
                ])
                continue
    
            elif bytecode == BYTECODE_ADD_SLOT:
                slot_type = bytecodes.pop(0)
                slot_type_str = {
                    SLOT_NORMAL: "SLOT_NORMAL",
                    SLOT_PARENT: "SLOT_PARENT",
                }[slot_type]
    
                disassembled.append([
                    index,
                    "ADD_SLOT",
                    "type:" + slot_type_str,
                ])
                continue
    
        return disassembled

Výsledek vypadá zabalený v samotné Selfové syntaxi například takto:

    (|
      literals = (| l <- dict clone. |
        l
          at: 0 Put: "ObjBox(Object(slots={benchmark: Object(slots={i: IntNumber(0), i:: AssignmentPrimitive()}, code=[Send(obj=Block(code=[Send(obj=Send(obj=Self(), msg=Message(i)), msg=BinaryMessage(name=<, parameter=IntNumber(1000000)))]), msg=KeywordMessage(name=whileTrue:, parameters=[Block(code=[Send(obj=Self(), msg=KeywordMessage(name=i:, parameters=[Send(obj=Send(obj=Self(), msg=Message(i)), msg=BinaryMessage(name=+, parameter=IntNumber(1)))]))])]))]), run_benchmark: Object(slots={start_time: Nil(), start_time:: AssignmentPrimitive(), end_time: Nil(), end_time:: AssignmentPrimitive()}, code=[Send(obj=Send(obj=Send(obj=Self(), msg=Message(primitives)), msg=Message(interpreter)), msg=KeywordMessage(name=runScript:, parameters=['objects/stdlib.tself'])), Send(obj=Self(), msg=KeywordMessage(name=start_time:, parameters=[Send(obj=Send(obj=Send(obj=Self(), msg=Message(primitives)), msg=Message(time)), msg=Message(timestamp))])), Send(obj=Self(), msg=Message(benchmark)), Send(obj=Self(), msg=KeywordMessage(name=end_time:, parameters=[Send(obj=Send(obj=Send(obj=Self(), msg=Message(primitives)), msg=Message(time)), msg=Message(timestamp))])), Send(obj=Send(obj=Send(obj=Send(obj=Send(obj=Self(), msg=Message(end_time)), msg=BinaryMessage(name=-, parameter=Send(obj=Self(), msg=Message(start_time)))), msg=Message(asString)), msg=BinaryMessage(name=+, parameter='
    ')), msg=Message(print))])}))";
          at: 1 Put: "StrBox(benchmark)";
          at: 2 Put: "ObjBox(Object(slots={i: IntNumber(0), i:: AssignmentPrimitive()}, code=[Send(obj=Block(code=[Send(obj=Send(obj=Self(), msg=Message(i)), msg=BinaryMessage(name=<, parameter=IntNumber(1000000)))]), msg=KeywordMessage(name=whileTrue:, parameters=[Block(code=[Send(obj=Self(), msg=KeywordMessage(name=i:, parameters=[Send(obj=Send(obj=Self(), msg=Message(i)), msg=BinaryMessage(name=+, parameter=IntNumber(1)))]))])]))]))";
          at: 3 Put: "StrBox(i)";
          at: 4 Put: "IntBox(0)";
          at: 5 Put: "StrBox(i:)";
          at: 6 Put: "StrBox(run_benchmark)";
          at: 7 Put: "ObjBox(Object(slots={start_time: Nil(), start_time:: AssignmentPrimitive(), end_time: Nil(), end_time:: AssignmentPrimitive()}, code=[Send(obj=Send(obj=Send(obj=Self(), msg=Message(primitives)), msg=Message(interpreter)), msg=KeywordMessage(name=runScript:, parameters=['objects/stdlib.tself'])), Send(obj=Self(), msg=KeywordMessage(name=start_time:, parameters=[Send(obj=Send(obj=Send(obj=Self(), msg=Message(primitives)), msg=Message(time)), msg=Message(timestamp))])), Send(obj=Self(), msg=Message(benchmark)), Send(obj=Self(), msg=KeywordMessage(name=end_time:, parameters=[Send(obj=Send(obj=Send(obj=Self(), msg=Message(primitives)), msg=Message(time)), msg=Message(timestamp))])), Send(obj=Send(obj=Send(obj=Send(obj=Send(obj=Self(), msg=Message(end_time)), msg=BinaryMessage(name=-, parameter=Send(obj=Self(), msg=Message(start_time)))), msg=Message(asString)), msg=BinaryMessage(name=+, parameter='
    ')), msg=Message(print))]))";
          at: 8 Put: "StrBox(start_time)";
          at: 9 Put: "StrBox(start_time:)";
          at: 10 Put: "StrBox(end_time)";
          at: 11 Put: "StrBox(end_time:)".
      ).
    
      disassembled = (||
        ("0", "PUSH_LITERAL", "type:OBJ", "index:0"), 
        ("3", "PUSH_LITERAL", "type:STR", "index:1"), 
        ("6", "PUSH_LITERAL", "type:OBJ", "index:2"), 
        ("9", "PUSH_LITERAL", "type:STR", "index:3"), 
        ("12", "PUSH_LITERAL", "type:INT", "index:4"), 
        ("15", "ADD_SLOT", "type:SLOT_NORMAL"), 
        ("17", "PUSH_LITERAL", "type:STR", "index:5"), 
        ("20", "PUSH_LITERAL", "type:ASSIGNMENT", "index:0"), 
        ("23", "ADD_SLOT", "type:SLOT_NORMAL"), 
        ("25", "ADD_SLOT", "type:SLOT_NORMAL"), 
        ("27", "PUSH_LITERAL", "type:STR", "index:6"), 
        ("30", "PUSH_LITERAL", "type:OBJ", "index:7"), 
        ("33", "PUSH_LITERAL", "type:STR", "index:8"), 
        ("36", "PUSH_LITERAL", "type:NIL", "index:0"), 
        ("39", "ADD_SLOT", "type:SLOT_NORMAL"), 
        ("41", "PUSH_LITERAL", "type:STR", "index:9"), 
        ("44", "PUSH_LITERAL", "type:ASSIGNMENT", "index:0"), 
        ("47", "ADD_SLOT", "type:SLOT_NORMAL"), 
        ("49", "PUSH_LITERAL", "type:STR", "index:10"), 
        ("52", "PUSH_LITERAL", "type:NIL", "index:0"), 
        ("55", "ADD_SLOT", "type:SLOT_NORMAL"), 
        ("57", "PUSH_LITERAL", "type:STR", "index:11"), 
        ("60", "PUSH_LITERAL", "type:ASSIGNMENT", "index:0"), 
        ("63", "ADD_SLOT", "type:SLOT_NORMAL"), 
        ("65", "ADD_SLOT", "type:SLOT_NORMAL"), 
        ("67", "PUSH_LITERAL", "type:STR", "index:6"), 
        ("70", "SEND", "type:UNARY", "params:0"), 
        ("73", "RETURN_TOP"), 
        ("74", "RETURN_TOP"), 
        ("75", "RETURN_TOP"), 
        ("76", "RETURN_TOP")
      ).
    
    bytecodes = (||
        3, 3, 0, 3, 2, 1, 3, 3, 2, 3, 2, 3, 3, 1, 4, 6, 0, 3, 2, 5, 3, 6, 0, 6, 0, 6, 0, 3, 2, 6, 3, 3, 7, 3, 2, 8, 3, 0, 0, 6, 0, 3, 2, 9, 3, 6, 0, 6, 0, 3, 2, 10, 3, 0, 0, 6, 0, 3, 2, 11, 3, 6, 0, 6, 0, 6, 0, 3, 2, 6, 0, 0, 0, 4, 4, 4, 4
    ).

Původně jsem měl výsledek obalen v JSONu, ale nakonec mi kamarád připoměl, že součástí experimentu s tinySelfem je vyzkoušet používat jeho *objektové literály*, čehož je výsledkem výše uvedený výpis.

Tedy interpreter vypisuje jako debug věci v syntaxi sama sebe. Nutno dodat, že zatím nevyzkoušený, neboť ve chvíli kdy byl tento blog napsán nebyly v tinySelfu podporovány ani pole, ani slovníky a jedná se tedy spíš jen o takový nástřel. Tomu taky napovídají ty AST stringy na začátku, které jsou silně nepřehledné, a které to bude chtít časem určitě vylepšit.

## Pokračování

Příště se už konečně podíváme jak vlastně uvnitř vypadá interpreter a smyčka vykonávání příkazů.