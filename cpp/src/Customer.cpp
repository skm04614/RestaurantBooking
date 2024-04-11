#include <string>

using std::string;

class Customer {
public:
	Customer(string name, string phoneNumber) {
		this->name = name;
		this->phoneNumber = phoneNumber;
	}

	Customer(string name, string phoneNumber, string email) {
		this->name = name;
		this->phoneNumber = phoneNumber;
		this->email = email;
	}

	string getEmail() {
		return email;
	}

private:
	string name;
	string phoneNumber;
	string email;
};
