import time
from typing import Dict, List, Union

class VotingMechanism:
    """Implements on-chain governance voting."""

    def __init__(self, voting_duration: int, quorum_percentage: float):
        """
        Initializes the voting mechanism.
        :param voting_duration: Duration of the voting period in seconds.
        :param quorum_percentage: Minimum percentage of total votes required for a proposal to be valid.
        """
        self.voting_duration = voting_duration
        self.quorum_percentage = quorum_percentage
        self.proposals = {}  # Stores proposals {proposal_id: {"title": str, "votes": Dict, "start_time": int}}

    def create_proposal(self, proposal_id: str, title: str):
        """
        Creates a new governance proposal.
        :param proposal_id: Unique identifier for the proposal.
        :param title: Title or description of the proposal.
        """
        if proposal_id in self.proposals:
            raise ValueError("Proposal ID already exists.")

        self.proposals[proposal_id] = {
            "title": title,
            "votes": {"yes": 0, "no": 0},
            "start_time": time.time(),
        }
        print(f"Proposal '{title}' created with ID: {proposal_id}")

    def cast_vote(self, proposal_id: str, vote: str, stake: float):
        """
        Casts a vote on a proposal.
        :param proposal_id: ID of the proposal to vote on.
        :param vote: Vote choice ('yes' or 'no').
        :param stake: Amount of stake used for the vote.
        """
        if proposal_id not in self.proposals:
            raise ValueError("Proposal not found.")

        if vote not in ["yes", "no"]:
            raise ValueError("Invalid vote choice. Must be 'yes' or 'no'.")

        proposal = self.proposals[proposal_id]
        if time.time() > proposal["start_time"] + self.voting_duration:
            raise ValueError("Voting period for this proposal has ended.")

        proposal["votes"][vote] += stake
        print(f"Vote cast: {stake} tokens for '{vote}' on proposal '{proposal_id}'")

    def get_results(self, proposal_id: str) -> Dict[str, Union[str, float, bool]]:
        """
        Calculates the results of a proposal.
        :param proposal_id: ID of the proposal to check results for.
        :return: A dictionary with the results.
        """
        if proposal_id not in self.proposals:
            raise ValueError("Proposal not found.")

        proposal = self.proposals[proposal_id]
        total_votes = proposal["votes"]["yes"] + proposal["votes"]["no"]
        quorum_met = total_votes >= (self.quorum_percentage / 100) * total_votes
        result = "yes" if proposal["votes"]["yes"] > proposal["votes"]["no"] else "no"

        return {
            "title": proposal["title"],
            "total_votes": total_votes,
            "yes_votes": proposal["votes"]["yes"],
            "no_votes": proposal["votes"]["no"],
            "quorum_met": quorum_met,
            "result": result if quorum_met else "quorum not met",
        }

    def get_active_proposals(self) -> List[str]:
        """
        Returns a list of active proposals.
        :return: List of active proposal IDs.
        """
        active_proposals = []
        for proposal_id, proposal in self.proposals.items():
            if time.time() <= proposal["start_time"] + self.voting_duration:
                active_proposals.append(proposal_id)
        return active_proposals


# Example usage
if __name__ == "__main__":
    # Initialize the voting mechanism with a 1-minute voting duration and 20% quorum
    voting_system = VotingMechanism(voting_duration=60, quorum_percentage=20)

    # Create proposals
    voting_system.create_proposal("proposal1", "Increase block size")
    voting_system.create_proposal("proposal2", "Reduce transaction fees")

    # Cast votes
    voting_system.cast_vote("proposal1", "yes", 100)
    voting_system.cast_vote("proposal1", "no", 50)
    voting_system.cast_vote("proposal2", "yes", 200)

    # Wait for the voting period to end
    time.sleep(61)

    # Get results
    print("\nResults for Proposal 1:", voting_system.get_results("proposal1"))
    print("Results for Proposal 2:", voting_system.get_results("proposal2"))

    # Get active proposals
    print("\nActive Proposals:", voting_system.get_active_proposals())
