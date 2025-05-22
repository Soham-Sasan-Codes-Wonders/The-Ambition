//By: Soham Sasan Gr. 12 																				2024/06/14
//Tic-Tac-Toe, The Java Edition!
import java.awt.*; //imports everything in the .awt class.

import java.awt.event.*; //imports everything in the .awt.event class.

import java.util.*; //imports everything in the .util class.

import javax.swing.*; //imports everything in the .swing class.

import javax.swing.Timer; //imports the Timer package.

public class mainFile implements ActionListener{ //implements the ActionListener (basically puts the functionality in the class).
	
	Random random = new Random(); //Creates and initializes a new Random variable (essentially, this variable will generate a random number and store it).
	
	JFrame frame = new JFrame(); //Creates a new JFrame window called frame.
	
	JPanel title_panel = new JPanel(); //Creates a new panel called title_panel.
	
	JPanel button_panel = new JPanel(); //Creates a new panel called button_panel.
	
	JLabel textfield = new JLabel(); //Creates a new JLabel called textfield.
	
	JButton[] buttons = new JButton[9]; //Creates 9 buttons.
	
	boolean player1; //Creates a new boolean called player1.
	
	boolean wplayer1; //Creates a new boolean called wplayer1.
	
	String name1; //Creates a new String called name1.
	
	String name2; //Creates a new String called name2.
	
	JButton playAgain = new JButton("Restart"); //Creates a new JButton called playAgain and puts the text 'Restart' on top of it.
	
	mainFile(){ //Creates a new Constructor class called mainFile.
		
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); //Sets the operation when the user closes the window (essentially, this will terminate the program once the user has closed the window).
		
		frame.setSize(1275,1050); //Sets the size of the JFrame (i.e., the window) to 1275 by 1050.
		
		frame.getContentPane().setBackground(new Color(25,20,65)); //Sets the background color of the window (JFrame).
		
		frame.setLayout(new BorderLayout()); //Sets the layout of the JFrame to BorderLayout.
		
		frame.setTitle("Tic-Tac-Toe - The Java Edition ;)"); //Sets the title of the window to Tic-Tac-Toe - The Java Edition ;). 
		
		frame.setVisible(true); //Sets the frame visibility to true.
		
		textfield.setBackground(new Color(100,25,65)); //Sets the background color of the textfield label.
		
		textfield.setForeground(new Color(25,255,0)); //Sets the foreground color of the textfield label.
		
		textfield.setFont(new Font("Ink Free", Font.BOLD,50)); //Defines the font of the textfield text to Ink Font.
		
		textfield.setVerticalAlignment(JLabel.NORTH); //Sets the vertical alignment of the textfield to North (at the top).
		
		textfield.setHorizontalAlignment(JLabel.CENTER); //Sets the horizontal alignment of the textfield to Center (in the middle).
		
		textfield.setText("Tic-Tac-Toe"); //Sets the text of textfield to Tic-Tac-Toe.
		
		textfield.setOpaque(true); //Sets the visibility of the textfield to true.
		
		title_panel.add(textfield, BorderLayout.NORTH); //Sets the position of the label to North (top of panel).
		
		title_panel.setLayout(new BorderLayout()); //Sets the layout of the title_panel to BorderLayout.
		
		title_panel.setBounds(0,0,1300,400); //Sets the boundary of the title_panel.
		
		title_panel.add(textfield); //Adds the textfield label to title_panel.
		
		frame.add(title_panel); //Adds the title_panel to the window (JFrame).
		
		button_panel.setLayout(new GridLayout(3,3)); //Sets the layout of the button_panel to GridLayout with 3 rows and 3 columns.
		
		button_panel.setBackground(new Color(150,150,25)); //Sets the background color of the button_panel.
		
		frame.add(button_panel); //Adds the button_panel to the window.
		
		frame.add(title_panel, BorderLayout.NORTH); //Sets the position of the title_panel to North (top of window).
		
		frame.add(button_panel, BorderLayout.CENTER); //Sets the position of the button_panel to Center (in the middle).

		for(int i = 0; i < 9; i++) { //For loop that runs as long as i is less than 9.
			
			buttons[i] = new JButton(); //Creates a new button with every iteration of the for loop. The index value of each button is specified by the value of i. 
			
			button_panel.add(buttons[i]); //Adds the button to button_panel.
			
			buttons[i].setFont(new Font("MV Boli", Font.BOLD,120)); //Sets the font of the buttons.
			
			buttons[i].setFocusable(false); //Allows the user to select the buttons (i.e., allows the buttons to be clicked).
			
			buttons[i].addActionListener(this); //Adds the ActionListener functionality to the buttons.
			
		}
		
		name1 = JOptionPane.showInputDialog(null, "What is your name?"); //Creates a popup asking the first user for their name. This is saved in name1.
		
		JOptionPane.showMessageDialog(null, "Thank you, " + name1 + "!" + " Who's the next player?"); //Creates a popup thanking the user and asking who is the second player.
		
		name2 = JOptionPane.showInputDialog(null, "What is your name?"); //Creates a popup asking the second user for their name. This is saved in name2.
		
		JOptionPane.showMessageDialog(null, "Thank you, " + name2 + "!"); //Creates a popup thanking the second user.
		
		JOptionPane.showMessageDialog(null, "Here are the rules of the game: "); //Creates a popup telling the users the rules of the game
		
		String[] rules = {"Rule 1: The order is at random; X or O could be first (will be shown on screen).", "Rule 2: First person to put their letter (either X or O) vertically, horizontally, or diagonally, wins!"}; //Creates a String array of rules.
		
		StringBuilder rulesText = new StringBuilder(); //Creates a variable called rulesText and initializes it.
		
        for (String rule : rules) { //An enhanced for loop that runs through every rule in the array.
        	
            rulesText.append(rule).append("\n"); //Appends each of the rules.
      
        }
        
        JOptionPane.showMessageDialog(null, rulesText.toString(), "Rules", JOptionPane.INFORMATION_MESSAGE); //Creates a popup that displays each of the rules.
        
        JOptionPane.showMessageDialog(null, "Let's play Tic-Tac-Toe!"); //Creates a popup that says 'Let's play Tic-Tac-Toe!'.
        
        title_panel.add(playAgain, BorderLayout.SOUTH); //Adds the playAgain button to title_panel and sets its position to SOUTH of the title_panel.
        
        playAgain.addActionListener(this); //Adds the ActionListener functionality to the playAgain button.
		
		firstTurn(); //calls the firstTurn method.
		
	}

	


	@Override
	public void actionPerformed(ActionEvent e) { //ActionPerformed Method (where the ActionListener gets its functionality from).
		
		if(e.getSource() == playAgain) { //Only runs if the user clicked the playAgain (i.e., Restart) button.
			
            resetGame(); //Calls on the resetGame method.
            
            textfield.setText("Restarted!"); //Sets the text of the textfield to Restarted.
            
            Timer timer = new Timer(1000, evt -> firstTurn()); //Creates a timer which delays the game from beginning again by 1000 ms.
            
            timer.setRepeats(false); //Specifies that the timer should not repeat again.
            
            timer.start(); //Starts the delay timer.
            
        }
		
		for(int i = 0; i < 9; i++) { //Creates a for loop that runs so long as i is less than 9.
			
			if(e.getSource() == buttons[i]) { //Only runs provided the ActionEvent retrieved the index of the button (any button).
				
				if(player1) { //Runs based on the condition of player1.
					
					if(buttons[i].getText() == "") { //Only runs if the text retrievd from the buttons is empty.
						
						buttons[i].setForeground(new Color(255,0,0)); //Sets the foreground color of the buttons.
						
						buttons[i].setText("X"); //Sets the text of the button to "X".
						
						player1 = false; //Sets the value of the player1 boolean to false.
						
						textfield.setText("It's your turn, " + name2 + " (O)"); //Sets the text of the textfield, telling the players that it the second player's turn.
						
						check(); //Calls the check method.
						
					}
					
				} else if(buttons[i].getText() == "") { //Only runs if the first if condition was not met. 
						
						buttons[i].setForeground(new Color(0,0,225)); //Sets the foreground color of the buttons.
						
						buttons[i].setText("O"); //Sets the text of the button to "O".
						
						player1 = true; //Sets the value of the player1 boolean to true.
						
						textfield.setText("It's your turn, " + name1 + " (X)"); //Sets the text of the textfield, telling the players that it is the first player's turn.
						
						check(); //Calls the check method.
						
					}
				
			} 
			
		}
		
	}
	
	
	public void firstTurn() { //firstTurn method.
		
		try { //Try-catch block, to delay the start of the game.
			
			Thread.sleep(1500); //Delays the start of the game.
			
		} catch (InterruptedException e) { //Handles any exceptions.
			
			e.printStackTrace(); //Handles this type of exception.
			
		}
		
		if(random.nextInt(2) == 0) { //Only runs if the integer value in random is 0.
			
			player1 = true; //Sets player1 boolean to true.
			
			textfield.setText("It's your turn, " + name1 + " (X)"); //Sets the text of textfield, telling the user that it is the first person's turn.
			
		} else { //If the above condition is not met, this runs.
			
			player1 = false; //Sets player1 boolean to false.
			
			textfield.setText("It's your turn, " + name2 + " (O)"); //Sets the text of tetfield, telling the user that it is the second person's turn.
			
		}
		
	}
	
	public void check() { //Check method.
		
		if((buttons[0]).getText() == "X" && (buttons[1]).getText() == "X" && (buttons[2]).getText() == "X") { //Checks to see if these specific buttons were pressed.
			
			xWins(0,1,2); //Passes these numbers into xWins method.
			
			return; //Returns result.
			
		}
		
		if((buttons[3]).getText() == "X" && (buttons[4]).getText() == "X" && (buttons[5]).getText() == "X") { //Checks to see if these specific buttons were pressed.
			
			xWins(3,4,5); //Passes these numbers into xWins method.
			
			return; //Returns result.
			
		}
		
		if((buttons[6]).getText() == "X" && (buttons[7]).getText() == "X" && (buttons[8]).getText() == "X") { //Checks to see if these specific buttons were pressed.
			
			xWins(6,7,8); //Passes these numbers into xWins method.
			
			return; //Returns result.
			
		}
		
		if((buttons[0]).getText() == "X" && (buttons[3]).getText() == "X" && (buttons[6]).getText() == "X") { //Checks to see if these specific buttons were pressed.
			
			xWins(0,3,6); //Passes these numbers into xWins method.
			
			return; //Returns result.
			
		}
		
		if((buttons[1]).getText() == "X" && (buttons[4]).getText() == "X" && (buttons[7]).getText() == "X") { //Checks to see if these specific buttons were pressed.
			
			xWins(1,4,7); //Passes these numbers into xWins method.
			
			return; //Returns result.
			
		}
		
		if((buttons[2]).getText() == "X" && (buttons[5]).getText() == "X" && (buttons[8]).getText() == "X") { //Checks to see if these specific buttons were pressed.
			
			xWins(2,5,8); //Passes these numbers into xWins method.
			
			return; //Returns result.
			
		}
		
		if((buttons[0]).getText() == "X" && (buttons[1]).getText() == "X" && (buttons[2]).getText() == "X") { //Checks to see if these specific buttons were pressed.
			
			xWins(0,1,2); //Passes these numbers into xWins method.
			
			return; //Returns result.
			
		}
		
		if((buttons[0]).getText() == "X" && (buttons[4]).getText() == "X" && (buttons[8]).getText() == "X") { //Checks to see if these specific buttons were pressed.
			
			xWins(0,4,8); //Passes these numbers into xWins method.
			
			return; //Returns result.
			
		}
		
		if((buttons[2]).getText() == "X" && (buttons[4]).getText() == "X" && (buttons[6]).getText() == "X") { //Checks to see if these specific buttons were pressed.
			
			xWins(2,4,6); //Passes these numbers into xWins method.
			
			return; //Returns result.
			
		}
		
		if((buttons[0]).getText() == "O" && (buttons[1]).getText() == "O" && (buttons[2]).getText() == "O") { //Checks to see if these specific buttons were pressed.
			
			oWins(0,1,2); //Passes these numbers into oWins method.
			
			return; //Returns result.
			
		}
		
		if((buttons[3]).getText() == "O" && (buttons[4]).getText() == "O" && (buttons[5]).getText() == "O") { //Checks to see if these specific buttons were pressed.
			
			oWins(3,4,5); //Passes these numbers into oWins method.
			
			return; //Returns result.
			
		}
		
		if((buttons[6]).getText() == "O" && (buttons[7]).getText() == "O" && (buttons[8]).getText() == "O") { //Checks to see if these specific buttons were pressed.
			
			oWins(6,7,8); //Passes these numbers into oWins method.
			
			return; //Returns result.
			
		}
		
		if((buttons[0]).getText() == "O" && (buttons[3]).getText() == "O" && (buttons[6]).getText() == "O") { //Checks to see if these specific buttons were pressed.
			
			oWins(0,3,6); //Passes these numbers into oWins method.
			
			return; //Returns result.
			
		}
		
		if((buttons[1]).getText() == "O" && (buttons[4]).getText() == "O" && (buttons[7]).getText() == "O") { //Checks to see if these specific buttons were pressed.
			
			oWins(1,4,7); //Passes these numbers into oWins method.
			
			return; //Returns result.
			
		}
		
		if((buttons[2]).getText() == "O" && (buttons[5]).getText() == "O" && (buttons[8]).getText() == "O") { //Checks to see if these specific buttons were pressed.
			
			oWins(2,5,8); //Passes these numbers into oWins method.
			
			return; //Returns result.
			
		}
		
		if((buttons[0]).getText() == "O" && (buttons[1]).getText() == "O" && (buttons[2]).getText() == "O") { //Checks to see if these specific buttons were pressed.
			
			oWins(0,1,2); //Passes these numbers into oWins method.
			
			return; //Returns result.
			
		}
		
		if((buttons[0]).getText() == "O" && (buttons[4]).getText() == "O" && (buttons[8]).getText() == "O") { //Checks to see if these specific buttons were pressed.
			
			oWins(0,4,8); //Passes these numbers into oWins method.
			
			return; //Returns result.
			
		}
		
		if((buttons[2]).getText() == "O" && (buttons[4]).getText() == "O" && (buttons[6]).getText() == "O") { //Checks to see if these specific buttons were pressed.
			
			oWins(2,4,6); //Passes these numbers into oWins method.
			
			return; //Returns result.
			
		}
		
		boolean tie = true; //Creates a new boolean called tie and sets it to true.
		
		for(JButton button: buttons) { //Creates an enhanced for loop that iterates through every button.
			
			if(button.getText().equals("")) { //Only runs if the text of the button equals a blank space.
				
				tie = false; //Sets boolean tie to false.
				
				break; //Exits out of the if statement.
				
			}
			
		}
		
		if(tie) { //Only runs if tie = true.
			
			textfield.setText("It's a tie!"); //Updates the textfield label to say that it is a tie.
			
		}
		
	}
	
	public void xWins(int a, int b, int c) { //Creates a xWins method that takes in three parameters (the three number combinations outlined in check method).
		
		wplayer1 = player1; //Sets the value of wplayer1 to the same value as player1 (either true or false).
		
		buttons[a].setBackground(Color.GREEN); //Sets the background color of the button to Green.
		
		buttons[b].setBackground(Color.GREEN); //Sets the background color of the button to Green.
		
		buttons[c].setBackground(Color.GREEN); //Sets the background color of the button to Green.
		
		for(int i = 0; i < 9; i++) { //Creates a for loop that runs so long as i is less than 9.
			
			buttons[i].setEnabled(false); //Disables the functionality of the buttons.
			
		}
		
		textfield.setText(name1 + " Wins!"); //Updates the textfield label, telling the players that the first player won.
		
	}
	
	public void oWins(int a, int b, int c) { //Creates an oWins method that takes in three parameters (the three number combinations outlined in check method).
		
		wplayer1 = player1; //Sets the value of wplayer1 to the same value as player1 (either true or false).
		
		buttons[a].setBackground(Color.GREEN); //Sets the background color of the button to Green.
		
		buttons[b].setBackground(Color.GREEN); //Sets the background color of the button to Green.
		
		buttons[c].setBackground(Color.GREEN); //Sets the background color of the button to Green.
		
		for(int i = 0; i < 9; i++) { //Creates a for loop that runs so long as i is less than 9.
			
			buttons[i].setEnabled(false); //Disables the functionality of the buttons.
			
		}
		
		textfield.setText(name2 + " Wins!"); //Updates the textfield label, telling the players that the second player won.
		
		
	}
	
	public void resetGame() { //Creates a resetGame method (to restart game).
		
	    for(int i = 0; i < 9; i++) { //Creates a for loop that runs so long as i is less than 9.
	    	
	        buttons[i].setText(""); //Sets the text of the buttons to blank (i.e., makes the buttons blank).
	        
	        buttons[i].setEnabled(true); //Restores the functionality of the buttons (allows the buttons to be clickable again).
	        
	        buttons[i].setBackground(new JButton().getBackground()); //Sets the background of the buttons to that of a blank button (not transparent).
	    }
	    
	    player1 = !wplayer1; //Sets the value of player1 to OPPOSITE of wplayer1 (if wplayer1 is true, player1 is false and vice versa). 
	    
	}
}
//ALL SOURCES USED TO MAKE THIS GAME: 

//YouTube:
//https://www.youtube.com/watch?v=rA7tfvpkw0I

//Generative AI:
//https://chatgpt.com/share/f3a47b90-690f-4890-a0da-136e52d4bc89
//https://chatgpt.com/share/cfa42c28-c814-4026-9e70-9f2085b7dbf9
//https://copilot.microsoft.com/sl/kFTYrB4SDVQ
//https://copilot.microsoft.com/sl/eZod9JfvmGi