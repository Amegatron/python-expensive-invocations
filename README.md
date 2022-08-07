Python's Expensive Method Invocations
==========

This tiny project is to demonstrate how expensive method invocations are
in Python and how crucial it may become.

First imagine you have some logic using a stack and initially you make it using "natural" Python lists:

```python
def natural_stack(length=9, iterations=200):
    stack = []
    stack.append(1)

    for i in range(iterations):
        for j in range(length - 1):
            stack.append(j)

        acc = 0
        while len(stack) > 0:
            acc += stack.pop()

        stack.append(acc)

    return stack.pop()
```

Nothing special here, it's just an arbitrary logic to make some computations using a stack. 
If I now benchmark this method on my PC, I will get such results (see `benchmark` method inside `src/main.py`):

```
Natural stack (pop/append):
  Real time: 4.195054
  CPU time:  4.187500
  Return value: 5601
```

Now I would like to optimize this method, and my assumption is that if I use a stack of a fixed size and not always pop/append,
but rather just shift an index (pointer) to the current top of the stack, it would be quicker:

```python
def index_shifted_stack(length=9, iterations=200):
    stack = list([None for x in range(length)])
    stack[0] = 1
    current_index = 0

    for i in range(iterations):
        for j in range(length - 1):
            current_index += 1
            stack[current_index] = j

        acc = 0
        while current_index >= 0:
            acc += stack[current_index]
            current_index -= 1

        current_index = 0
        stack[current_index] = acc

    return stack[0]
```

Indeed, if I benchmark this method now, I will get significantly better results:

```
Index shift (inline):
  Real time: 2.377122
  CPU time:  2.375000
  Return value: 5601
```

Cool! I think this solution is good enough - we cut the total time almost by half! But I don't want to always have such
mess everytime I need this stack. So, let's encapsulate it in a separate class `QuickerStack`.
And have another test just to make sure we're alright:

```python
from src.QuickerStack import QuickerStack

def quicker_stack(length=9, iterations=200):
    stack = QuickerStack(length)
    stack.push(1)

    for i in range(iterations):
        for j in range(length - 1):
            stack.push(j)

        acc = 0
        while len(stack) > 0:
            acc += stack.pop()

        stack.push(acc)

    return stack.pop()
```

Alright, the code is now almost exactly the same as the first one. Let's benchmark it:

```
Index shift (encapsulated):
  Real time: 9.872037
  CPU time:  9.859375
  Return value: 5601
```

What? But, I just wanted to optimize the function ...
![](media/bummer.jpg)

The problem is exactly in method invocations of our new QuickerStack class. And in this particular
example, it not only didn't optimize the initial function. It slowed it down twice.

In general, there is no surprise that additional method invocations add some overhead to overall time.
But here we get an increase of almost 4X to base logic by just encapsulating it in a separate class.

See also an explanation of [why it so huge](https://stackoverflow.com/a/54524575/2054918) in Python.