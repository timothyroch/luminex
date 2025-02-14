import time
from typing import Dict, List, Union


class ProposalSubmission:
    """Handles submission and management of governance proposals."""

    def __init__(self, min_deposit: float, submission_fee: float, deposit_refund_time: int):
        """
        Initializes the ProposalSubmission system.
        :param min_deposit: Minimum deposit required to submit a proposal.
        :param submission_fee: Fee charged for submitting a proposal.
        :param deposit_refund_time: Time (in seconds) after which deposits can be refunded.
        """
        self.min_deposit = min_deposit
        self.submission_fee = submission_fee
        self.deposit_refund_time = deposit_refund_time
        self.proposals = {}  # Stores proposals {proposal_id: {"title": str, "deposit": float, "submitted_at": int, "status": str}}
        self.refundable_deposits = {}  # Tracks refundable deposits {proposal_id: deposit_amount}

    def submit_proposal(self, proposal_id: str, title: str, deposit: float) -> str:
        """
        Submits a new governance proposal.
        :param proposal_id: Unique identifier for the proposal.
        :param title: Title or description of the proposal.
        :param deposit: Amount of deposit provided by the proposer.
        :return: Confirmation message.
        """
        if proposal_id in self.proposals:
            raise ValueError("Proposal ID already exists.")

        if deposit < self.min_deposit:
            raise ValueError(f"Deposit must be at least {self.min_deposit} tokens.")

        # Register the proposal
        self.proposals[proposal_id] = {
            "title": title,
            "deposit": deposit - self.submission_fee,
            "submitted_at": time.time(),
            "status": "pending"
        }
        self.refundable_deposits[proposal_id] = deposit - self.submission_fee
        return f"Proposal '{title}' submitted successfully with ID: {proposal_id}"

    def update_status(self, proposal_id: str, status: str):
        """
        Updates the status of a proposal.
        :param proposal_id: ID of the proposal to update.
        :param status: New status (e.g., 'approved', 'rejected', 'expired').
        """
        if proposal_id not in self.proposals:
            raise ValueError("Proposal not found.")

        self.proposals[proposal_id]["status"] = status
        print(f"Proposal '{proposal_id}' status updated to: {status}")

    def refund_deposit(self, proposal_id: str) -> Union[str, float]:
        """
        Refunds the deposit for a proposal if eligible.
        :param proposal_id: ID of the proposal for which the deposit should be refunded.
        :return: Refund amount or a message if not eligible.
        """
        if proposal_id not in self.proposals:
            raise ValueError("Proposal not found.")

        proposal = self.proposals[proposal_id]
        time_elapsed = time.time() - proposal["submitted_at"]

        if proposal["status"] not in ["rejected", "expired"]:
            raise ValueError("Deposit can only be refunded for rejected or expired proposals.")

        if time_elapsed < self.deposit_refund_time:
            remaining_time = self.deposit_refund_time - time_elapsed
            return f"Deposit refund not yet available. Please wait {remaining_time:.2f} seconds."

        refund_amount = self.refundable_deposits.pop(proposal_id, 0.0)
        print(f"Deposit of {refund_amount} tokens refunded for proposal '{proposal_id}'.")
        return refund_amount

    def get_proposal(self, proposal_id: str) -> Dict:
        """
        Retrieves the details of a specific proposal.
        :param proposal_id: ID of the proposal to retrieve.
        :return: Proposal details.
        """
        if proposal_id not in self.proposals:
            raise ValueError("Proposal not found.")
        return self.proposals[proposal_id]

    def list_proposals(self) -> List[Dict]:
        """
        Lists all submitted proposals.
        :return: A list of proposals with their details.
        """
        return list(self.proposals.values())


# Example usage
if __name__ == "__main__":
    # Initialize with example parameters
    proposal_manager = ProposalSubmission(min_deposit=100, submission_fee=10, deposit_refund_time=60)

    # Submit proposals
    print(proposal_manager.submit_proposal("proposal1", "Increase block size", 150))
    print(proposal_manager.submit_proposal("proposal2", "Reduce transaction fees", 120))

    # Get details of a proposal
    print("\nProposal Details:", proposal_manager.get_proposal("proposal1"))

    # Update proposal status
    proposal_manager.update_status("proposal1", "rejected")

    # Wait for refund eligibility
    time.sleep(61)
    print("\nRefund Status:", proposal_manager.refund_deposit("proposal1"))

    # List all proposals
    print("\nAll Proposals:", proposal_manager.list_proposals())
