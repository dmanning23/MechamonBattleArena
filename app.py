
import os
import streamlit as st
from mechamonGenerator import MechamonGenerator
from battleGenerator import BattleGenerator
from dalleImageGenerator import DalleImageGenerator
from sdImageGenerator import SdImageGenerator
from keys import openAIapikey

def displayMechamon(mechamon):
    st.header(mechamon.name)
    st.markdown(mechamon.appearance)
    st.markdown(mechamon.description)
    st.subheader("Abilities:")
    for ability in mechamon.abilities:
        st.markdown(f"{ability.name}: {ability.description}")

def displayBattle(battle):
    st.header("BATTLE!!!")
    st.subheader(battle.setup)
    for action in battle.attacks:
        st.markdown(f"{action.description} {action.result}")
    st.markdown(battle.climax)
    st.subheader(f"WINNER: {battle.winner}!")

def main():
    #os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    os.environ["OPENAI_API_KEY"] = openAIapikey

    st.set_page_config(
        page_title="Mechamon Battle Arena",
        page_icon="🤖⚔️🤖")
    
    container = st.container()
    with container:

        mechamonGenerator = MechamonGenerator()
        battleGenerator = BattleGenerator()
        #imageGenerator = DalleImageGenerator()
        imageGenerator = SdImageGenerator()
        
        with st.form(key="my form", clear_on_submit=False):

            #Player 1 text entry
            player1  = st.text_area(label="Player 1, choose your Mechamon!", key="p1", height = 200)

            #Allow the user to provide a resume:
            player2  = st.text_area(label="Player 2, choose your Mechamon!", key="p2", height = 200)
            
            #Add a button to generate the cover letter
            submit_button = st.form_submit_button(label="BATTLE!!!")

            merge_button = st.form_submit_button(label="MERGE!!!")

        if submit_button:

            #Check that the first player provided a mechamon
            if not player1:
                st.error("Player 1 is not ready")

            #Check that the second player provided a mechamon
            if not player2:
                st.error("Player 2 is not ready")

            if player1 and player2:

                #Create the first Mechamon
                with st.spinner("Creating Player 1 Mechamon..."):
                    mecha1 = mechamonGenerator.Generate(player1)
                    displayMechamon(mecha1)

                #with st.spinner(f"Creating {mecha1.name} artwork..."):
                    #art1 = imageGenerator.CreateImage(mecha1.appearance)
                    #st.image(art1)

                #Create the second Mechamon
                with st.spinner("Creating Player 2 Mechamon..."):
                    mecha2 = mechamonGenerator.Generate(player2)
                    displayMechamon(mecha2)

                #with st.spinner(f"Creating {mecha1.name} artwork..."):
                    #art2 = imageGenerator.CreateImage(mecha2.appearance)
                    #st.image(art2)

                #Make them fight!
                with st.spinner("BATTLING!!!"):
                    battle = battleGenerator.Battle(mecha1, mecha2)
                    displayBattle(battle)

        if merge_button:

            #Check that the first player provided a mechamon
            if not player1:
                st.error("Player 1 is not ready")

            #Check that the second player provided a mechamon
            if not player2:
                st.error("Player 2 is not ready")

            if player1 and player2:

                #Create the first Mechamon
                with st.spinner("Creating Player 1 Mechamon..."):
                    mecha1 = mechamonGenerator.Generate(player1)
                    displayMechamon(mecha1)

                #with st.spinner(f"Creating {mecha1.name} artwork..."):
                    #art1 = imageGenerator.CreateImage(mecha1.appearance)
                    #st.image(art1)

                #Create the second Mechamon
                with st.spinner("Creating Player 2 Mechamon..."):
                    mecha2 = mechamonGenerator.Generate(player2)
                    displayMechamon(mecha2)

                #with st.spinner(f"Creating {mecha2.name} artwork..."):
                    #art2 = imageGenerator.CreateImage(mecha2.appearance)
                    #st.image(art2)

                #Make them fight!
                with st.spinner("MERGING!!!"):
                    mecha3 = mechamonGenerator.Merge(mecha1, mecha2)

                st.header("MERGED!!!")
                displayMechamon(mecha3)
                
                #with st.spinner(f"Creating {mecha3.name} artwork..."):
                    #art3 = imageGenerator.CreateImage(mecha3.appearance)
                    #st.image(art3)

if __name__ == "__main__":
    main()
