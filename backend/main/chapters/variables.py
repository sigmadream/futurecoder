import ast
import re

from astcheck import is_ast_like

from main.text import Page
from main.text import Step, VerbatimStep


class IntroducingVariables(Page):

    class word_assign(VerbatimStep):
        """
To make interesting programs, we can't always manipulate the same values. We need a way to refer to values that are unknown ahead of time and can change - values that can vary. These are called *variables*.

Run this code:

__program_indented__
        """

        program = "word = 'Hello'"

    class word_check(VerbatimStep):
        """
This creates a variable with the name `word` that refers to the string value `'Hello'`.

Check now that this is true by simply running `__program__` in the shell by itself.
        """

        program = "word"

    class word_string_check(VerbatimStep):
        """
Good. For comparison, run `__program__` in the shell by itself, with the quotes.
        """

        program = "'word'"

    class sunshine_undefined_check(VerbatimStep):
        """
As you can see, the quotes make all the difference. `'word'` is literally just `'word'`, hence it's technically called a *string literal*. On the other hand, `word` is a variable, whose value may be anything.

Similarly, `'sunshine'` is `'sunshine'`, but what's `__program__` without quotes?
        """

        program = "sunshine"

    final_text = """
The answer is that `sunshine` looks like a variable, so Python tries to look up its value, but since we never defined a variable with that name we get an error.
"""


class UsingVariables(Page):
    def before_step(self):
        if 'word_plus_name' in self.step_name and self.console.locals.get("word") != "Hello":
            return dict(
                message="Oops, you need to set `word = 'Hello'` before we can continue."
            )

    class name_assign(Step):
        """
Previously we made a variable called `word` with the value `'Hello'` with this code:

    word = 'Hello'

Now make a variable called `name` whose value is another string. The string can be anything...how about your name?
        """

        def check(self):
            match = re.match(r"(.*)=", self.input)
            if match and match.group(1).strip() != "name":
                return dict(message="Put `name` before the `=` to create a variable called `name`.")

            if self.input_matches("name=[^'\"].*"):
                return dict(message="You've got the `name = ` part right, now put a string on "
                                    "the right of the `=`.")

            if not is_ast_like(
                    self.tree,
                    ast.Module(body=[ast.Assign(targets=[ast.Name(id='name')],
                                                value=ast.Constant())])
            ):
                return False
            name = self.console.locals.get('name')
            if isinstance(name, str):
                if not name:
                    return dict(message="Choose a non-empty string")
                if name[0] == " ":
                    return dict(message="For this exercise, choose a name "
                                        "that doesn't start with a space.")

                return True

    class hello_plus_name(VerbatimStep):
        """
You can use variables in calculations just like you would use literals. For example, try:

__program_indented__
        """

        program = "'Hello ' + name"

    class word_plus_name(VerbatimStep):
        """
Or you can just add variables together. Try:

    __program_indented__
        """

        program = "word + name"

    class word_plus_name_with_space(VerbatimStep):
        """
Oops...that doesn't look nice. Can you modify the code above so that there's a space between the word and the name?
        """

        hints = """
You will need to use `+` twice, like 1+2+3.
Your answer should contain a mixture of variables (no quotes) and string literals (quotes).
You will need to have a space character inside quotes.
        """

        expected_program = "word + ' ' + name"

    class word_assign_goodbye(VerbatimStep):
        """
Perfect!

Variables can also change their values over time. Right now `word` has the value `'Hello'`. You can change its value in the same way that you set it for the first time. Run this:

    __program_indented__
        """

        program = "word = 'Goodbye'"

    class goodbye_plus_name(VerbatimStep):
        """
Now observe the effect of this change by running `__program__` again.
        """

        program = "word + ' ' + name"

    class first_print(VerbatimStep):
        """
Those quotes around strings are getting annoying. Try running this:

    __program_indented__
        """

        program = "print(word + ' ' + name)"

    final_text = """
Hooray! No more quotes! We'll break down what's happening in this code later. For now just know that `print(<something>)` displays `<something>` in the shell. In particular it displays the actual content of strings that we usually care about, instead of a representation of strings that's suitable for code which has things like quotes. The word `print` here has nothing to do with putting ink on paper.
"""


class WritingPrograms(Page):

    class editor_hello_world(VerbatimStep):
        """
It's time to stop doing everything in the shell. In the top right you can see the *editor*. This is a place where you can write and run longer programs. The shell is great and you should keep using it to explore, but the editor is where real programs live.

Copy the program below into the editor, then click the 'Run' button:

    __program_indented__
        """

        def program(self):
            word = 'Hello'
            name = 'World'
            print(word + ' ' + name)
            word = 'Goodbye'
            print(word + ' ' + name)

    final_text = """
Congratulations, you have run your first actual program!

Take some time to understand this program. Python runs each line one at a time from top to bottom. You should try simulating this process in your head - think about what each line does. See how the value of `word` was changed and what effect this had. Note that when `print` is used multiple times, each thing (`Hello World` and `Goodbye World` in this case) is printed on its own line.

Some things to note about programs in the editor:

1. The program runs in the shell, meaning that the variables defined in the program now exist in the shell with the last values they had in the program. This lets you explore in the shell after the program completes. For example, `name` now has the value `'World'` in the shell.
2. Programs run in isolation - they don't depend on any previously defined variables. The shell is reset and all previous variables are cleared. So even though `word` currently exists in the shell, if you delete the first line of the program and run it again, you'll get an error about `word` being undefined.
3. If you enter code in the shell and it has a value, that value will automatically be displayed. That doesn't happen for programs in the editor - you have to print values. If you remove `print()` from the program, changing the two lines to just `word + ' ' + name`, nothing will be displayed.

I recommend that you check all of these things for yourself.
"""


class StoringCalculationsInVariables(Page):

    class sentence_equals_word_plus_name(VerbatimStep):
        """
Often you will use variables to store the results of calculations. This will help to build more complex programs. For example, try this program:

    __program_indented__
        """

        def program(self):
            word = 'Hello'
            name = 'World'
            sentence = word + ' ' + name
            print(sentence)

    class sentence_doesnt_change(VerbatimStep):
        """
Now `sentence` has the value `'Hello World'` which can be used multiple times. Note that it will continue to have this value until it is directly reassigned, e.g. with another statement like `sentence = <something>`. For example, add these two lines to the end of the program:

    word = 'Goodbye'
    print(sentence)
        """

        # noinspection PyUnusedLocal
        def expected_program(self):
            word = 'Hello'
            name = 'World'
            sentence = word + ' ' + name
            print(sentence)
            word = 'Goodbye'
            print(sentence)

    final_text = """
Unlike a spreadsheet where formulas update automatically, a variable like `sentence` doesn't remember how it was calculated and won't change if the underlying values `word` or `name` are changed.
"""
