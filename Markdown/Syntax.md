[[#Print statements]]
[[#Variable declaration]]
[[#Comments]]
[[#Operations]]
[[#Functions]]
[[#Graphics]]

# Print statements
**To console**
```python
print(f"Hello, {name}")
```

**To window**
```python
!println -> f"Hello, {name}", id="greeting"
```

**Here, id cannot have space.**
****
# Variable declaration
**Compatible types**
1. String
2. Int
3. float
4. UO (User-defined Object)

```python
greeting: str = "Hello, World"
an_int: int = 3
value_of_pi: float = 3.1415
```

****
# Comments
``` python
# This is a comment
```

****
# Operations
**Arithmetic operations**

```python
print(f"{an_int + value_of_pi}")
!println -> f"{an_int + value_of_pi} this value is on the console", id="a_value"
```

**Logic operators**
``` python
print(f"{an_int == value_of_pi}")
!println -> f"{an_int >= value_of_pi} this value is on the console", id="a_value"
```

****

# Functions
```python
def get_sum(numOne: int, numTwo: int) -> int:
	return numOne + numTwo

!println -> get_sum(1, 2), id="the_sum"
```

****

# Graphics
[[#Set window properties]]
[[#Set text properties]]

#### Set window properties
``` python
!window -> {
		   background-color: black; // default white
		   color: white; // default black
		   width: 800; // default in px
		   height: 800; // default in px
}
```

#### Set text properties
```python
!{the_sum, greeting} -> {
					  color: red;
					  font-size: 16px;
					  background-color: black;
					  text-align: center;
					  position: absolute;
					  left: 50%;
					  top: 50%;
					  right: 50%;
					  bottom: 50%;
					  font-family: "Arial"
}
```

