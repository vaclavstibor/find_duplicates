Dobrý den,

## 1.
v první řadě dokažte, že vaše řešení splňuje zadání:

_Your solution must also work on other input data of the same size with similar number of duplicates._

Jinými slovy, že jste jen nehledal parametry, které náhodnou fungují pouze na daných testech.

### Odpověď:



## 2.
```python
def select_filter(line):
    # Select a Bloom filter based on the hash of the line
    return int(hashlib.md5(line.encode()).hexdigest(), 16) % num_bloom_filters


filter_index = select_filter(line)

bloom_filter = bloom_filters[filter_index]
```

Proč má tato struktura lepší vlastnosti než klasické Bloom filtry?

### Odpověď:


---

### 1. **Rovnoměrné rozložení do filtrů**
Rovnice:  
\[
\text{filter\_index} = \text{hash(line)} \mod \text{num\_bloom\_filters}
\]

- **Argument:** `num_bloom_filters = 7` (prvočíslo) zajišťuje rovnoměrné rozdělení položek mezi filtry. 
- **Test:** U datového generátoru ověř rovnoměrnost distribuce:
  - Pro každou položku spočítej `filter_index` a sleduj počet výskytů v každém filtru.
  - Očekává se, že distribuce bude rovnoměrná (± několik % kvůli náhodnosti hashování).

---

### 2. **Optimalita počtu hashovacích funkcí \( k \)**
Rovnice:  
\[
k_\text{opt} = \frac{m}{n} \cdot \ln(2)
\]

- **Hodnoty:**  
  - \( m = \text{bloom\_capacity} = 4{,}000{,}000 \),  
  - \( n \): Odhad počtu unikátních položek ve filtru.
- **Výpočet:** Ověř, zda \( num\_hashes = 12 \) je blízko optimální hodnotě:
\[
k_\text{opt} = \frac{4{,}000{,}000}{\text{expected\_n}} \cdot \ln(2)
\]

#### Testy:

\[
m = 16{,}000{,}000, \quad n = 1{,}000{,}000 \quad \Rightarrow \quad k_\text{opt} \approx 9.6
\]

---

### 3. **Pravděpodobnost falešného pozitivu \( P \)**
Rovnice:  
\[
P = \left(1 - \exp\left(-\frac{k \cdot n}{m}\right)\right)^k
\]

- **Hodnoty:**  
  - \( k = 12 \),  
  - \( n = \text{expected\_n} \),  
  - \( m = 4{,}000{,}000 \).
- **Test:** Vypočítej \( P \) pro očekávané \( n \). Pokud \( P \) je přijatelně malé (např. < 0.01), je volba parametrů vhodná.

---

### 4. **Lineární nezávislost hashovacích funkcí**
Rovnice:  
\[
h_i(x) = h_1(x) + i \cdot h_2(x) \mod m
\]

- **Argument:** MD5 a SHA-1 jsou použity pro generování dvou základních hashů. Přidáním \( i \cdot h_2(x) \) dochází k variaci, což je standardní postup pro Bloom filtry.

---

### 5. **Kapacita jednotlivých filtrů**
Rovnice:  
\[
m' = \frac{\text{bloom\_capacity}}{\text{num\_bloom\_filters}}
\]

- **Výpočet:** \( m' = \frac{4{,}000{,}000}{7} \approx 571{,}428 \).  
- **Test:** Ověř, zda každý filtr efektivně zvládá svůj podíl \( n' = \frac{n}{\text{num\_bloom\_filters}} \) unikátních položek.

---

### Testy pro konkrétní data
1. Generuj položky z `DataGenerator` a loguj, kolik z nich skončí v každém filtru.
2. Vypočítej optimální hodnotu \( k_\text{opt} \) a porovnej s použitou hodnotou \( k = 12 \).
3. Vypočítej pravděpodobnost falešného pozitivu \( P \) pro očekávaný počet položek \( n \).

Chceš-li, mohu dodat konkrétní skript na testování těchto rovnic s tvými daty.